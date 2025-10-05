# Testing Guide - UI Navigation Updates

## Quick Start

### Running the Frontend

1. **Navigate to the UI directory:**
   ```bash
   cd gradio/ui/clinic-intellect-main
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   - The app will typically run on `http://localhost:5173`
   - Or check the terminal output for the exact URL

### Running the Backend (Django)

1. **Navigate to the patient system directory:**
   ```bash
   cd patient_system
   ```

2. **Run the Django server:**
   ```bash
   python manage.py runserver
   ```

3. **Backend will be available at:**
   - `http://localhost:8000`

## Testing the New Back Button Features

### Test 1: Back Button from Input Page
**Steps:**
1. Click "Start Analysis" on home page
2. You should see the Input page with a **Back button** at the top-left
3. Select any input mode (Database/Upload/Text)
4. Click the **Back button**
5. **Expected:** Return to Home page, all input fields cleared

**Pass Criteria:**
- ✅ Back button is visible and clickable
- ✅ Returns to Home page
- ✅ All input fields are reset

### Test 2: File Upload State Management
**Steps:**
1. Click "Start Analysis"
2. Select "Upload" mode
3. Upload a file (any .txt, .pdf, or image file)
4. Verify file name appears below the upload area
5. Click the **Back button**
6. Click "Start Analysis" again
7. Select "Upload" mode again
8. **Expected:** No file should be shown (upload area should be empty)

**Pass Criteria:**
- ✅ File uploads successfully
- ✅ File name displays after upload
- ✅ Back button clears the uploaded file
- ✅ Re-entering shows clean upload area

### Test 3: Back Button from Processing Page
**Steps:**
1. Start Analysis → Input page
2. Enter a Patient ID (e.g., "1")
3. Click "Fetch Data"
4. While on the Processing page, click the **Back button**
5. **Expected:** Return to Input page with previous input preserved

**Pass Criteria:**
- ✅ Back button visible on Processing page
- ✅ Returns to Input page
- ✅ Uploaded file state is cleared

### Test 4: Back Button from Results Page
**Steps:**
1. Complete a full workflow (Home → Input → Processing → Results)
2. On Results page, verify **Back button** is visible at top-left
3. Click the **Back button**
4. **Expected:** Return to Input page, all results cleared

**Pass Criteria:**
- ✅ Back button visible on Results page
- ✅ Returns to Input page
- ✅ Patient data cleared
- ✅ AI summary cleared
- ✅ Uploaded file cleared

### Test 5: Text Input Mode
**Steps:**
1. Start Analysis → Input page
2. Select "Text" mode
3. Paste some medical text
4. Click "Generate Summary"
5. View results
6. Click **Back button**
7. **Expected:** Return to Input page, text preserved but results cleared

**Pass Criteria:**
- ✅ Text input works correctly
- ✅ Summary generates
- ✅ Back button returns to Input page
- ✅ Previous results are cleared

### Test 6: Upload Mode with Different File Types
**Steps:**
1. Test with .txt file
2. Click Back, then re-enter
3. Test with .pdf file
4. Click Back, then re-enter
5. Test with image file (.jpg, .png)
6. **Expected:** Each time, file should be cleared when going back

**Pass Criteria:**
- ✅ All supported file types upload correctly
- ✅ Back button clears file state for all types
- ✅ No memory leaks or stale file references

### Test 7: Home Button (Header)
**Steps:**
1. Navigate to any page (Input, Processing, or Results)
2. Click the "Home" button in the header
3. **Expected:** Return to Home page, all state cleared

**Pass Criteria:**
- ✅ Home button works from all pages
- ✅ All state is reset (including uploaded files)
- ✅ Clean slate for new workflow

### Test 8: Multiple Workflow Cycles
**Steps:**
1. Complete full workflow: Home → Input → Results → Back → Input
2. Upload a file
3. Go Back
4. Enter text instead
5. Generate summary
6. Go Back
7. Use database mode
8. **Expected:** Each transition should clear previous state properly

**Pass Criteria:**
- ✅ No stale data between workflows
- ✅ Each mode works independently
- ✅ No file upload remnants
- ✅ No performance degradation

## Visual Checks

### Back Button Styling
- ✅ Consistent appearance across all pages
- ✅ ArrowLeft icon visible
- ✅ "Back" text label present
- ✅ Hover effect works (glass-card-hover style)
- ✅ Rounded corners (rounded-2xl)
- ✅ Proper spacing and alignment

### Responsive Design
Test on different screen sizes:
- ✅ Desktop (1920x1080)
- ✅ Tablet (768x1024)
- ✅ Mobile (375x667)

## Common Issues to Check

### Issue 1: File Not Clearing
**Symptom:** Uploaded file still shows after clicking Back
**Check:** Verify `setUploadedFile(null)` is called in navigation functions

### Issue 2: Back Button Not Visible
**Symptom:** Back button doesn't appear
**Check:** Verify component is receiving `onBack` prop

### Issue 3: Wrong Page Navigation
**Symptom:** Back button goes to wrong page
**Check:** Verify correct callback function is passed

## Performance Testing

### Memory Leak Check
1. Upload large file (5-10 MB)
2. Click Back
3. Open browser DevTools → Memory tab
4. Take heap snapshot
5. Verify file is not retained in memory

### Navigation Speed
- ✅ Back button responds immediately
- ✅ No lag when clearing state
- ✅ Smooth page transitions

## Browser Compatibility

Test in:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (if available)

## API Integration Testing

### With Backend Running
1. Test database mode with real patient IDs
2. Test file upload with actual file processing
3. Test text mode with AI summary generation
4. Verify Back button works correctly with API calls in progress

## Regression Testing

Ensure existing features still work:
- ✅ AI summary generation
- ✅ Patient data display
- ✅ File upload and processing
- ✅ Text input processing
- ✅ Database retrieval
- ✅ Save functionality
- ✅ Toast notifications

## Sign-Off Checklist

- [ ] All 8 test scenarios passed
- [ ] Visual checks completed
- [ ] Responsive design verified
- [ ] No memory leaks detected
- [ ] Browser compatibility confirmed
- [ ] API integration working
- [ ] No regressions found
- [ ] Documentation updated

## Reporting Issues

If you find any issues, please document:
1. Test scenario number
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Browser and version
6. Screenshots (if applicable)
