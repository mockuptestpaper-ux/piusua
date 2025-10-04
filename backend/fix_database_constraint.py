#!/usr/bin/env python3
"""
Script to fix the database constraint to allow SUB and NAT question types
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
import sys

# Load environment variables
load_dotenv('.env')

# Supabase connection
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_ANON_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def fix_database_constraint():
    """Fix the database constraint to allow SUB and NAT question types"""
    try:
        # Try to execute SQL to drop the old constraint and create a new one
        # This is the SQL we want to run:
        sql_commands = [
            "ALTER TABLE new_questions DROP CONSTRAINT IF EXISTS new_questions_question_type_check;",
            "ALTER TABLE new_questions ADD CONSTRAINT new_questions_question_type_check CHECK (question_type IN ('MCQ', 'MSQ', 'NAT', 'SUB'));"
        ]
        
        for sql in sql_commands:
            print(f"Executing: {sql}")
            try:
                result = supabase.rpc('execute_sql', {'sql': sql}).execute()
                print(f"Success: {result}")
            except Exception as e:
                print(f"Error executing SQL: {e}")
                # Try alternative approach using postgrest
                return False
        
        return True
        
    except Exception as e:
        print(f"Error fixing constraint: {e}")
        return False

def test_constraint_fix():
    """Test if we can now insert SUB questions"""
    try:
        # Try to insert a test SUB question
        import uuid
        test_question = {
            "id": str(uuid.uuid4()),
            "topic_id": "7c583ed3-64bf-4fa0-bf20-058ac4b40737",  # Using a known topic ID from test results
            "question_statement": "Test SUB question for constraint verification",
            "question_type": "SUB",
            "options": None,
            "answer": "Test subjective answer",
            "solution": "Test solution",
            "difficulty_level": "Medium",
            "created_at": "2025-01-27T10:00:00Z",
            "updated_at": "2025-01-27T10:00:00Z"
        }
        
        result = supabase.table("new_questions").insert(test_question).execute()
        
        if result.data:
            print("SUCCESS: SUB question type constraint is fixed!")
            # Clean up - delete the test question
            supabase.table("new_questions").delete().eq("id", test_question["id"]).execute()
            return True
        else:
            print("FAILED: Could not insert SUB question")
            return False
            
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    print("Attempting to fix database constraint...")
    
    # First test if the constraint is already fixed
    if test_constraint_fix():
        print("Constraint is already working correctly!")
        sys.exit(0)
    
    print("Constraint needs fixing. Attempting repair...")
    success = fix_database_constraint()
    
    if success:
        print("Constraint fix applied. Testing...")
        if test_constraint_fix():
            print("DATABASE CONSTRAINT SUCCESSFULLY FIXED!")
        else:
            print("Constraint fix applied but test still fails")
    else:
        print("Could not fix constraint via SQL. Using workaround approach.")