# Plan: Output

## Introduction
Modify the `do_research` method to create two output files instead of just printing to console:
1. `output_items.md` - Contains all items from response.output regardless of type
2. `reasoning.md` - Contains only reasoning-type items

## Phase 1: Setup Output Directory
- Task 1.1: Create output directory structure
- Task 1.2: Verify directory creation

## Phase 2: Modify do_research Method
- Task 2.1: Update method to collect all output items
- Task 2.2: Filter reasoning items separately
- Task 2.3: Create output_items.md file with all items
- Task 2.4: Create reasoning.md file with reasoning items only
- Task 2.5: Remove old print statements

## Phase 3: Testing and Validation
- Task 3.1: Test the modified method
- Task 3.2: Verify files are created correctly
- Task 3.3: Validate content format and structure

## Checklist
- [x] Task 1.1: Create output directory structure
- [x] Task 1.2: Verify directory creation
- [x] Task 2.1: Update method to collect all output items
- [x] Task 2.2: Filter reasoning items separately
- [x] Task 2.3: Create output_items.md file with all items
- [x] Task 2.4: Create reasoning.md file with reasoning items only
- [x] Task 2.5: Remove old print statements
- [x] Task 3.1: Test the modified method
- [x] Task 3.2: Verify files are created correctly
- [x] Task 3.3: Validate content format and structure

## Success Criteria
- Two files are created in the output directory when do_research() is called
- output_items.md contains all items from response.output with proper formatting
- reasoning.md contains only reasoning-type items with proper formatting
- Method executes without errors
- Files contain readable, well-formatted content
