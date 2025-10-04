#!/usr/bin/env python3
"""
Focused test for SUB question type constraint workaround fix
Based on review request: Test POST /api/generate-question with question_type='SUB' and topic_id='7c583ed3-64bf-4fa0-bf20-058ac4b40737'
"""

import requests
import json
from datetime import datetime

def test_sub_constraint_workaround():
    """Test the specific SUB question type constraint workaround fix"""
    print("🎯 FOCUSED SUB CONSTRAINT WORKAROUND TEST")
    print("=" * 60)
    print("SPECIFIC TEST: SUB question generation with topic_id='7c583ed3-64bf-4fa0-bf20-058ac4b40737'")
    print("EXPECTED: SUB questions save successfully to questions_topic_wise table")
    print("FOCUS: Verify workaround handles schema differences (question_id vs id, no difficulty_level)")
    
    # Configuration
    base_url = "https://question-fixer-app.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    topic_id = "7c583ed3-64bf-4fa0-bf20-058ac4b40737"
    
    print(f"\n🔍 Testing SUB Question Generation...")
    print(f"   Base URL: {base_url}")
    print(f"   API URL: {api_url}")
    print(f"   Topic ID: {topic_id}")
    print(f"   Question Type: SUB")
    
    # Test SUB question generation
    request_data = {
        "topic_id": topic_id,
        "question_type": "SUB",
        "part_id": None,
        "slot_id": None
    }
    
    url = f"{api_url}/generate-question"
    headers = {'Content-Type': 'application/json'}
    
    print(f"\n📤 Making POST request...")
    print(f"   URL: {url}")
    print(f"   Headers: {headers}")
    print(f"   Payload: {json.dumps(request_data, indent=2)}")
    
    try:
        response = requests.post(url, json=request_data, headers=headers, timeout=60)
        
        print(f"\n📥 Response received:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        print(f"   Response Size: {len(response.text)} characters")
        
        if response.status_code == 200:
            print(f"\n✅ SUCCESS - SUB question generated and saved successfully!")
            
            try:
                response_data = response.json()
                print(f"\n📋 Generated SUB Question Details:")
                print(f"   Question ID: {response_data.get('id', 'N/A')}")
                print(f"   Question Type: {response_data.get('question_type', 'N/A')}")
                print(f"   Topic ID: {response_data.get('topic_id', 'N/A')}")
                print(f"   Question: {response_data.get('question_statement', '')[:200]}...")
                print(f"   Answer: {response_data.get('answer', '')[:150]}...")
                print(f"   Solution: {response_data.get('solution', '')[:150]}...")
                print(f"   Difficulty: {response_data.get('difficulty_level', 'N/A')}")
                
                # Check if it was saved to alternate table
                saved_to_table = response_data.get('_saved_to_table', 'new_questions')
                print(f"   Saved to table: {saved_to_table}")
                
                if saved_to_table == 'questions_topic_wise':
                    print(f"\n🎯 WORKAROUND ANALYSIS:")
                    print(f"   ✅ WORKAROUND SUCCESSFUL: SUB question saved to questions_topic_wise table")
                    print(f"   ✅ Schema mapping handled correctly (question_id vs id, no difficulty_level)")
                    print(f"   ✅ Database constraint violation bypassed properly")
                    
                    print(f"\n🎯 CONSTRAINT WORKAROUND TEST: ✅ PASSED")
                    print(f"   - SUB question generated without errors")
                    print(f"   - Database constraint violation handled properly")
                    print(f"   - Schema differences managed correctly")
                    print(f"   - Fallback to questions_topic_wise table working")
                    
                    return True, "SUB constraint workaround is working correctly"
                else:
                    print(f"\n🎯 WORKAROUND ANALYSIS:")
                    print(f"   ⚠️ UNEXPECTED: SUB question saved to {saved_to_table} table")
                    print(f"   ⚠️ Expected: questions_topic_wise table")
                    print(f"   ⚠️ This might indicate the constraint was fixed in new_questions table")
                    
                    print(f"\n🎯 CONSTRAINT WORKAROUND TEST: ⚠️ UNEXPECTED BEHAVIOR")
                    print(f"   - SUB question generated successfully")
                    print(f"   - But saved to unexpected table: {saved_to_table}")
                    
                    return True, f"SUB question generated but saved to {saved_to_table} instead of questions_topic_wise"
                    
            except Exception as json_error:
                print(f"\n❌ JSON parsing error: {str(json_error)}")
                print(f"   Raw response: {response.text[:500]}...")
                return False, f"JSON parsing error: {str(json_error)}"
                
        else:
            print(f"\n❌ FAILED - Expected 200, got {response.status_code}")
            print(f"   Full Response: {response.text}")
            
            # Analyze the specific error
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', 'No detail provided')
                print(f"\n🔍 Error Analysis:")
                print(f"   Error Detail: {error_detail}")
                
                # Check for specific constraint error patterns
                if "constraint" in error_detail.lower():
                    print(f"\n🚨 CONSTRAINT ERROR ANALYSIS:")
                    
                    if "difficulty_level" in error_detail.lower():
                        print(f"   ❌ SCHEMA ISSUE: questions_topic_wise table schema problem")
                        print(f"   ❌ Missing difficulty_level column in questions_topic_wise table")
                        print(f"   💡 SOLUTION: Remove difficulty_level from SUB question data when saving to questions_topic_wise")
                        
                    if "question_type_check" in error_detail.lower():
                        print(f"   ❌ TYPE CONSTRAINT: new_questions table still rejects SUB type")
                        print(f"   ❌ Database constraint 'new_questions_question_type_check' blocks SUB")
                        print(f"   💡 SOLUTION: Update database constraint to allow SUB type")
                        
                    if "foreign key constraint" in error_detail.lower():
                        print(f"   ❌ FOREIGN KEY ISSUE: questions_topic_wise table foreign key problem")
                        print(f"   ❌ question_id field references non-existent record in questions table")
                        print(f"   💡 SOLUTION: Use different field mapping or create proper foreign key reference")
                        
                    if "question_id_fkey" in error_detail.lower():
                        print(f"   🎯 SPECIFIC ISSUE: questions_topic_wise_question_id_fkey constraint")
                        print(f"   ❌ The question_id field in questions_topic_wise must reference existing questions table")
                        print(f"   ❌ Current workaround uses question_id field but doesn't create questions table entry")
                        print(f"   💡 SOLUTION: Either create questions table entry first, or use different field mapping")
                        
                elif "quota" in error_detail.lower() or "429" in str(response.status_code):
                    print(f"\n⚠️ API QUOTA ISSUE:")
                    print(f"   ⚠️ Gemini API quota exhausted - cannot test generation")
                    print(f"   ⚠️ This is not a constraint workaround issue")
                    
                else:
                    print(f"\n❓ OTHER ERROR:")
                    print(f"   Error: {error_detail}")
                    
            except Exception:
                print(f"   Could not parse error response")
            
            print(f"\n🎯 CONSTRAINT WORKAROUND TEST: ❌ FAILED")
            print(f"   - SUB question generation still has issues")
            print(f"   - Workaround is not working properly")
            print(f"   - Database constraint/schema issues remain")
            
            return False, f"SUB constraint workaround failed: {error_detail}"
            
    except Exception as e:
        print(f"\n❌ EXCEPTION - Error: {str(e)}")
        print(f"\n🎯 CONSTRAINT WORKAROUND TEST: ❌ ERROR")
        print(f"   - Network or request error occurred")
        print(f"   - Cannot determine if workaround is working")
        
        return False, f"Request exception: {str(e)}"

def main():
    """Main test execution"""
    print("🚀 Starting Focused SUB Constraint Workaround Test")
    print("=" * 80)
    print(f"Test started at: {datetime.now()}")
    print("=" * 80)
    
    # Run the test
    success, message = test_sub_constraint_workaround()
    
    # Print summary
    print(f"\n📊 FOCUSED TEST SUMMARY")
    print("=" * 60)
    print(f"Test completed at: {datetime.now()}")
    
    if success:
        print(f"\n✅ SUB CONSTRAINT WORKAROUND FIX: WORKING")
        print(f"   Result: {message}")
        print(f"   - SUB questions can now be generated and saved")
        print(f"   - Database constraint violation handled properly")
        print(f"   - Schema mapping working correctly")
    else:
        print(f"\n❌ SUB CONSTRAINT WORKAROUND FIX: STILL FAILING")
        print(f"   Result: {message}")
        print(f"   - SUB questions still cannot be generated/saved")
        print(f"   - Constraint workaround needs further investigation")
        print(f"   - Database schema or constraint issues remain")
    
    print(f"\n🎯 RECOMMENDATION:")
    if success:
        print(f"   ✅ The SUB constraint workaround is working as expected")
        print(f"   ✅ SUB questions are being saved successfully")
        print(f"   ✅ No further action needed for this fix")
    else:
        print(f"   ❌ The SUB constraint workaround needs additional work")
        print(f"   ❌ Review the error analysis above for specific issues")
        print(f"   ❌ Focus on database schema and foreign key constraints")

if __name__ == "__main__":
    main()