# Plan: Tokens

## Phase 1: Analysis and Design
- Task 1.1: Analyze current output processor structure
- Task 1.2: Investigate OpenAI response object for token usage data
- Task 1.3: Design token metrics extraction approach
- Task 1.4: Plan integration with existing time metrics

## Phase 2: Implementation
- Task 2.1: Add token extraction function
- Task 2.2: Modify process_response_output to extract tokens
- Task 2.3: Update header formatting to include token metrics
- Task 2.4: Test with existing output files

## Phase 3: Testing and Validation
- Task 3.1: Create test cases for token extraction
- Task 3.2: Validate output format matches requirements
- Task 3.3: Test with different response types

## Checklist
- [x] Task 1.1: Analyze current output processor structure
- [x] Task 1.2: Investigate OpenAI response object for token usage data
- [x] Task 1.3: Design token metrics extraction approach
- [x] Task 1.4: Plan integration with existing time metrics
- [x] Task 2.1: Add token extraction function
- [x] Task 2.2: Modify process_response_output to extract tokens
- [x] Task 2.3: Update header formatting to include token metrics
- [ ] Task 2.4: Test with existing output files
- [ ] Task 3.1: Create test cases for token extraction
- [ ] Task 3.2: Validate output format matches requirements
- [ ] Task 3.3: Test with different response types

## Success Criteria
- Token usage metrics are extracted from OpenAI response objects
- Output file header includes both time taken and token usage
- Format is consistent and readable
- No breaking changes to existing functionality
- Token metrics are displayed at the top of output files similar to time taken
