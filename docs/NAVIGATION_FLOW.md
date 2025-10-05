# Application Navigation Flow

## Updated Navigation Structure with Back Buttons

```
┌─────────────────────────────────────────────────────────────────┐
│                          HOME PAGE                              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  🏠 MedRecord AI                                       │    │
│  │  Revolutionary healthcare analytics powered by AI      │    │
│  │                                                         │    │
│  │              [Start Analysis] ──────────┐             │    │
│  │                                          │             │    │
│  └──────────────────────────────────────────┼─────────────┘    │
│                                             │                   │
└─────────────────────────────────────────────┼───────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT PAGE                              │
│                                                                 │
│  [◄ Back]  ◄─── NEW! Clears all state, returns to Home        │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  Choose Input Method:                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│  │  │ Database │  │  Upload  │  │   Text   │           │    │
│  │  └──────────┘  └──────────┘  └──────────┘           │    │
│  │                                                        │    │
│  │  Input Area:                                          │    │
│  │  ┌────────────────────────────────────────────┐      │    │
│  │  │ [Patient ID / File Upload / Text Input]    │      │    │
│  │  └────────────────────────────────────────────┘      │    │
│  │                                                        │    │
│  │              [Fetch Data / Generate Summary] ─────┐   │    │
│  └────────────────────────────────────────────────────┼──┘    │
│                                                        │        │
└────────────────────────────────────────────────────────┼────────┘
                                                         │
                                                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING PAGE                            │
│                                                                 │
│  [◄ Back]  ◄─── NEW! Returns to Input, clears file state      │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │                    ⚙️ Processing                       │    │
│  │                                                         │    │
│  │              🔄 AI Processing Data...                  │    │
│  │         Analyzing medical information                  │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       RESULTS PAGE                              │
│                                                                 │
│  [◄ Back]  ◄─── NEW! Returns to Input, clears all results     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  📊 Medical Analysis                                   │    │
│  │                                                         │    │
│  │  Patient Profile | Contact Info | AI Summary          │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │    │
│  │  │   Name      │  │   Phone     │  │  Generate   │   │    │
│  │  │   Age       │  │   Email     │  │  Summary    │   │    │
│  │  │   Gender    │  │   Address   │  │  [Button]   │   │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │    │
│  │                                                         │    │
│  │  Medical History | Checkups | Lab Tests | Treatments  │    │
│  │                                                         │    │
│  │              [Save Report]                             │    │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## State Management Flow

### State Variables Tracked
```typescript
- currentStep: "home" | "input" | "processing" | "results"
- inputMode: "database" | "upload" | "text"
- patientId: string
- textInput: string
- uploadedFile: File | null  ◄─── KEY: Cleared on back navigation
- patientData: PatientData | null
- aiSummary: string
- isProcessing: boolean
```

### Navigation Functions

#### 1. `resetWorkflow()` - From Any Page to Home
```typescript
Clears:
✓ currentStep → "home"
✓ patientData → null
✓ aiSummary → ""
✓ patientId → ""
✓ textInput → ""
✓ uploadedFile → null  ◄─── NEW!
```

#### 2. `goBackToInput()` - From Processing/Results to Input
```typescript
Clears:
✓ currentStep → "input"
✓ patientData → null
✓ aiSummary → ""
✓ uploadedFile → null  ◄─── NEW!

Preserves:
✓ patientId (for database mode)
✓ textInput (for text mode)
✓ inputMode
```

#### 3. `goBackToHome()` - From Input to Home
```typescript
Clears:
✓ currentStep → "home"
✓ patientData → null
✓ aiSummary → ""
✓ patientId → ""
✓ textInput → ""
✓ uploadedFile → null  ◄─── NEW!
```

## User Journey Examples

### Journey 1: Database Mode
```
1. Home → Click "Start Analysis"
2. Input → Select "Database" → Enter Patient ID "1"
3. Input → Click "Fetch Data"
4. Processing → (Auto-transition)
5. Results → View patient data
6. Results → Click [◄ Back]
7. Input → (Patient ID preserved, file cleared)
8. Input → Can modify or fetch different patient
```

### Journey 2: File Upload Mode
```
1. Home → Click "Start Analysis"
2. Input → Select "Upload" → Upload "report.pdf"
3. Input → Click "Generate Summary"
4. Processing → (Auto-transition)
5. Results → View AI summary
6. Results → Click [◄ Back]
7. Input → (File cleared! Upload area empty) ◄─── KEY IMPROVEMENT
8. Input → Can upload different file
```

### Journey 3: Text Input Mode
```
1. Home → Click "Start Analysis"
2. Input → Select "Text" → Paste medical report
3. Input → Click "Generate Summary"
4. Processing → (Auto-transition)
5. Results → View AI summary
6. Results → Click [◄ Back]
7. Input → (Text preserved, results cleared)
8. Input → Can modify text and regenerate
```

### Journey 4: Changing Input Modes
```
1. Home → Click "Start Analysis"
2. Input → Select "Upload" → Upload file
3. Input → Click [◄ Back]
4. Home → Click "Start Analysis"
5. Input → Select "Text" → (Previous file NOT shown) ◄─── KEY
6. Input → Paste text → Generate
7. Results → Click [◄ Back]
8. Input → (File still cleared, text preserved)
```

## Header Navigation

```
┌─────────────────────────────────────────────────────────┐
│  🧠 MedRecord AI                        [🏠 Home]       │
│     Healthcare Analytics Platform                       │
└─────────────────────────────────────────────────────────┘
                                            ▲
                                            │
                                    Available on all pages
                                    except Home page
                                    Clears ALL state
```

## Memory Management

### Before (Problem)
```
User uploads file → Navigates back → File still in memory
User uploads new file → Old file + new file in memory
Multiple cycles → Memory leak!
```

### After (Solution)
```
User uploads file → Navigates back → File cleared from memory ✓
User uploads new file → Only new file in memory ✓
Multiple cycles → No memory accumulation ✓
```

## Edge Cases Handled

1. **Back during processing:**
   - User can cancel and return to input
   - File state is cleared
   - No orphaned API calls

2. **Multiple back clicks:**
   - Each back button goes to correct previous page
   - State is consistently cleared

3. **Browser refresh:**
   - All state resets to initial
   - No stale data persists

4. **Switching input modes:**
   - File cleared when switching from Upload mode
   - Each mode starts fresh

## Benefits Summary

✅ **Better UX:** Intuitive back navigation on every page
✅ **Memory Efficient:** Files properly cleared from memory
✅ **Clean State:** No stale data between workflows
✅ **Error Recovery:** Easy to go back and fix mistakes
✅ **Consistent:** Same back button pattern everywhere
✅ **Accessible:** Clear visual indicators and labels
✅ **Responsive:** Works on all screen sizes
✅ **Fast:** Instant navigation, no delays
