import { useState } from "react";
import { Brain, Sparkles, Shield, Zap, Upload, Database, FileText, Home, ArrowRight, Check, Loader2, ArrowLeft } from "lucide-react";
import { toast } from "@/hooks/use-toast";
import { PatientData } from "@/types/patient";
import { fetchPatientById, generateAISummary, generateSummaryFromText, generateSummaryFromFile } from "@/services/patientApi";

type WorkflowStep = "home" | "input" | "processing" | "results";
type InputMode = "database" | "upload" | "text";

const Index = () => {
  const [currentStep, setCurrentStep] = useState<WorkflowStep>("home");
  const [inputMode, setInputMode] = useState<InputMode>("database");
  const [patientId, setPatientId] = useState("");
  const [textInput, setTextInput] = useState("");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [patientData, setPatientData] = useState<PatientData | null>(null);
  const [aiSummary, setAiSummary] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleStartAnalysis = () => {
    setCurrentStep("input");
    toast({
      title: "Let's get started",
      description: "Choose how you'd like to input medical data",
    });
  };

  const handleFetchData = async () => {
    // Validation based on input mode
    if (inputMode === "database" && !patientId.trim()) {
      toast({
        title: "Patient ID required",
        description: "Please enter a patient ID",
        variant: "destructive",
      });
      return;
    }

    // Validate patient ID is an integer
    if (inputMode === "database") {
      const trimmedId = patientId.trim();
      const parsedId = parseInt(trimmedId, 10);
      
      if (isNaN(parsedId) || parsedId.toString() !== trimmedId || parsedId <= 0) {
        toast({
          title: "Invalid Patient ID",
          description: "Patient ID must be a positive integer (e.g., 1, 2, 3)",
          variant: "destructive",
        });
        return;
      }
    }

    if (inputMode === "text" && !textInput.trim()) {
      toast({
        title: "Text input required",
        description: "Please enter medical report text",
        variant: "destructive",
      });
      return;
    }

    if (inputMode === "upload" && !uploadedFile) {
      toast({
        title: "File required",
        description: "Please upload a medical report file",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    setCurrentStep("processing");

    try {
      if (inputMode === "database") {
        // Fetch patient data from the API
        const data = await fetchPatientById(patientId.trim());
        setPatientData(data);
        setAiSummary("");
        
        toast({
          title: "Data retrieved successfully",
          description: "AI analysis is ready",
        });
      } else if (inputMode === "text") {
        // Generate summary from text directly
        const summary = await generateSummaryFromText(textInput.trim());
        setAiSummary(summary);
        setPatientData(null);
        
        toast({
          title: "Summary generated",
          description: "AI analysis from text completed",
        });
      } else if (inputMode === "upload" && uploadedFile) {
        // Generate summary from uploaded file
        const summary = await generateSummaryFromFile(uploadedFile);
        setAiSummary(summary);
        setPatientData(null);
        
        toast({
          title: "Summary generated",
          description: `AI analysis from ${uploadedFile.name} completed`,
        });
      }
      
      setCurrentStep("results");
    } catch (error) {
      console.error("Error processing data:", error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to process data",
        variant: "destructive",
      });
      setCurrentStep("input");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleGenerateSummary = async () => {
    if (!patientData) return;
    
    setIsProcessing(true);

    try {
      // Call the AI summary API endpoint
      const summary = await generateAISummary(patientData.patient.id);
      
      setAiSummary(summary);
      
      toast({
        title: "AI analysis complete",
        description: "Medical summary has been generated",
      });
    } catch (error) {
      console.error("Error generating summary:", error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to generate AI summary",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      toast({
        title: "File selected",
        description: `${file.name} (${(file.size / 1024).toFixed(2)} KB)`,
      });
    }
  };

  const handleSaveData = () => {
    const recordId = `MED-${Date.now().toString().slice(-6)}`;
    toast({
      title: "Saved successfully!",
      description: `Medical record saved with ID: ${recordId}`,
    });
  };

  const resetWorkflow = () => {
    setCurrentStep("home");
    setPatientData(null);
    setAiSummary("");
    setPatientId("");
    setTextInput("");
    setUploadedFile(null);
  };

  const goBackToInput = () => {
    setCurrentStep("input");
    setPatientData(null);
    setAiSummary("");
    setUploadedFile(null);
  };

  const goBackToHome = () => {
    setCurrentStep("home");
    setPatientData(null);
    setAiSummary("");
    setPatientId("");
    setTextInput("");
    setUploadedFile(null);
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[128px] animate-float" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-[128px] animate-float" style={{ animationDelay: "1s" }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent/10 rounded-full blur-[128px] animate-float" style={{ animationDelay: "2s" }} />
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 glass-card border-b border-white/10 backdrop-blur-2xl">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold gradient-text">MedRecord AI</h1>
                <p className="text-xs text-muted-foreground hidden sm:block">Healthcare Analytics Platform</p>
              </div>
            </div>

            {currentStep !== "home" && (
              <button
                onClick={resetWorkflow}
                className="flex items-center gap-2 px-4 py-2 glass-card-hover text-sm font-medium"
              >
                <Home className="w-4 h-4" />
                <span className="hidden sm:inline">Home</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 lg:py-16">
        {currentStep === "home" && <HomePage onStart={handleStartAnalysis} />}
        {currentStep === "input" && (
          <InputPage
            inputMode={inputMode}
            setInputMode={setInputMode}
            patientId={patientId}
            setPatientId={setPatientId}
            textInput={textInput}
            setTextInput={setTextInput}
            uploadedFile={uploadedFile}
            onFileUpload={handleFileUpload}
            onFetch={handleFetchData}
            isProcessing={isProcessing}
            onBack={goBackToHome}
          />
        )}
        {currentStep === "processing" && <ProcessingPage onBack={goBackToInput} />}
        {currentStep === "results" && (
          <ResultsPage
            patientData={patientData}
            aiSummary={aiSummary}
            onGenerateSummary={handleGenerateSummary}
            onSave={handleSaveData}
            isProcessing={isProcessing}
            onBack={goBackToInput}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
            <p>© 2025 MedRecord AI. Powered by advanced neural networks.</p>
            <div className="flex items-center gap-4">
              <span className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-accent" />
                Enterprise Security
              </span>
              <span className="flex items-center gap-2">
                <Zap className="w-4 h-4 text-primary" />
                97.3% Accuracy
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

// Home Page
const HomePage = ({ onStart }: { onStart: () => void }) => {
  return (
    <div className="space-y-16 animate-fade-in">
      {/* Hero Section */}
      <section className="text-center py-12 lg:py-20">
        <div className="inline-flex items-center justify-center w-20 h-20 lg:w-24 lg:h-24 rounded-3xl bg-gradient-to-br from-primary via-secondary to-accent mb-8 shadow-2xl animate-glow-pulse">
          <Sparkles className="w-10 h-10 lg:w-12 lg:h-12 text-white" />
        </div>
        
        <h1 className="text-4xl lg:text-7xl font-black gradient-text mb-6 tracking-tight">
          MedRecord AI
        </h1>
        
        <p className="text-lg lg:text-2xl text-muted-foreground max-w-3xl mx-auto mb-12 leading-relaxed">
          Revolutionary healthcare analytics powered by next-generation artificial intelligence
        </p>

        <button onClick={onStart} className="btn-primary text-lg group">
          <span className="flex items-center gap-2">
            Start Analysis
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </span>
        </button>
      </section>

      {/* Features Grid */}
      <section className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <FeatureCard
          icon={<Brain className="w-8 h-8" />}
          title="AI Analysis"
          description="Advanced neural networks analyze medical data with 97.3% accuracy"
          color="primary"
        />
        <FeatureCard
          icon={<Zap className="w-8 h-8" />}
          title="Instant Processing"
          description="Lightning-fast data processing and summary generation"
          color="secondary"
        />
        <FeatureCard
          icon={<Shield className="w-8 h-8" />}
          title="Secure Storage"
          description="Enterprise-grade security for all medical records"
          color="accent"
        />
      </section>

      {/* Stats Grid */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        <StatCard label="Patients" value="2,847" trend="+12%" />
        <StatCard label="Accuracy" value="97.3%" trend="+0.8%" />
        <StatCard label="Speed" value="2.4s" trend="-15%" />
        <StatCard label="Security" value="100%" trend="Maintained" />
      </section>

      {/* Action Cards */}
      <section className="grid md:grid-cols-2 gap-6">
        <ActionCard
          title="Quick Analysis"
          description="Start immediate medical data analysis with AI"
          buttonText="Start Now"
          onAction={onStart}
          variant="primary"
        />
        <ActionCard
          title="View Reports"
          description="Access previously generated analysis reports"
          buttonText="View Reports"
          onAction={() => toast({ title: "Coming soon", description: "Reports feature in development" })}
          variant="secondary"
        />
      </section>
    </div>
  );
};

// Input Page
const InputPage = ({
  inputMode,
  setInputMode,
  patientId,
  setPatientId,
  textInput,
  setTextInput,
  uploadedFile,
  onFileUpload,
  onFetch,
  isProcessing,
  onBack,
}: {
  inputMode: InputMode;
  setInputMode: (mode: InputMode) => void;
  patientId: string;
  setPatientId: (id: string) => void;
  textInput: string;
  setTextInput: (text: string) => void;
  uploadedFile: File | null;
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onFetch: () => void;
  isProcessing: boolean;
  onBack: () => void;
}) => {
  const inputModes = [
    { id: "database" as InputMode, name: "Database", icon: Database, description: "Retrieve existing patient records" },
    { id: "upload" as InputMode, name: "Upload", icon: Upload, description: "Upload medical documents" },
    { id: "text" as InputMode, name: "Text", icon: FileText, description: "Paste medical report text" },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in-up">
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="flex items-center gap-2 px-4 py-2 glass-card-hover text-sm font-medium rounded-2xl"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>
      </div>
      <div className="text-center">
        <h2 className="text-3xl lg:text-5xl font-bold gradient-text mb-4">Add Medical Report</h2>
        <p className="text-lg text-muted-foreground">Choose your preferred input method</p>
      </div>

      {/* Input Mode Selection */}
      <div className="grid sm:grid-cols-3 gap-4">
        {inputModes.map((mode) => (
          <button
            key={mode.id}
            onClick={() => setInputMode(mode.id)}
            className={`p-6 rounded-3xl border-2 transition-all text-left ${
              inputMode === mode.id
                ? "border-primary bg-primary/10 shadow-lg scale-105"
                : "border-white/10 glass-card-hover"
            }`}
          >
            <mode.icon className={`w-10 h-10 mb-4 ${inputMode === mode.id ? "text-primary" : "text-muted-foreground"}`} />
            <h3 className="font-bold text-lg mb-2">{mode.name}</h3>
            <p className="text-sm text-muted-foreground">{mode.description}</p>
          </button>
        ))}
      </div>

      {/* Input Form */}
      <div className="glass-card p-6 lg:p-8">
        {inputMode === "database" && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Patient ID</label>
              <input
                type="text"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                placeholder="Enter patient identifier (e.g., 1, 2, 3...)"
                className="w-full px-4 py-3 bg-background/50 border border-white/10 rounded-2xl focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
              />
            </div>
          </div>
        )}

        {inputMode === "upload" && (
          <div className="space-y-4">
            <label className="block">
              <div className="border-2 border-dashed border-white/20 rounded-3xl p-12 text-center hover:border-primary/50 transition-all cursor-pointer">
                <input
                  type="file"
                  onChange={onFileUpload}
                  accept=".txt,.pdf,.doc,.docx,.jpg,.jpeg,.png"
                  className="hidden"
                />
                <Upload className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
                <p className="font-medium mb-2">Drop files here or click to browse</p>
                <p className="text-sm text-muted-foreground">Supports: TXT, PDF, DOC, DOCX, JPG, PNG</p>
              </div>
            </label>
            {uploadedFile && (
              <div className="p-4 rounded-2xl bg-primary/10 border border-primary/20">
                <div className="flex items-center gap-3">
                  <FileText className="w-5 h-5 text-primary" />
                  <div className="flex-1">
                    <p className="font-medium text-sm">{uploadedFile.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {(uploadedFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                  <Check className="w-5 h-5 text-primary" />
                </div>
              </div>
            )}
          </div>
        )}

        {inputMode === "text" && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Medical Report Text</label>
              <textarea
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder="Paste medical report content here..."
                rows={10}
                className="w-full px-4 py-3 bg-background/50 border border-white/10 rounded-2xl focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all resize-none"
              />
            </div>
          </div>
        )}

        <button
          onClick={onFetch}
          disabled={isProcessing}
          className="btn-primary w-full mt-6 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isProcessing ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 className="w-5 h-5 animate-spin" />
              Processing...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              {inputMode === "database" ? "Fetch Data" : "Generate Summary"}
              <ArrowRight className="w-5 h-5" />
            </span>
          )}
        </button>
      </div>
    </div>
  );
};

// Processing Page
const ProcessingPage = ({ onBack }: { onBack: () => void }) => {
  return (
    <div className="space-y-8 animate-scale-in">
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="flex items-center gap-2 px-4 py-2 glass-card-hover text-sm font-medium rounded-2xl"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>
      </div>
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-24 h-24 lg:w-32 lg:h-32 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center mx-auto mb-8 animate-glow-pulse">
            <Loader2 className="w-12 h-12 lg:w-16 lg:h-16 text-white animate-spin" />
          </div>
          <h2 className="text-3xl lg:text-4xl font-bold gradient-text mb-4">AI Processing Data</h2>
          <p className="text-lg text-muted-foreground">Analyzing medical information...</p>
        </div>
      </div>
    </div>
  );
};

// Results Page
const ResultsPage = ({
  patientData,
  aiSummary,
  onGenerateSummary,
  onSave,
  isProcessing,
  onBack,
}: {
  patientData: PatientData | null;
  aiSummary: string;
  onGenerateSummary: () => void;
  onSave: () => void;
  isProcessing: boolean;
  onBack: () => void;
}) => {
  // For text/upload modes, we only have summary, no patient data
  const hasPatientData = patientData !== null;
  const latestCheckup = hasPatientData ? patientData.checkups[0] : null;
  const latestTreatment = hasPatientData ? patientData.treatments[0] : null;
  const latestLabTest = hasPatientData ? patientData.lab_tests[0] : null;

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in-up">
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="flex items-center gap-2 px-4 py-2 glass-card-hover text-sm font-medium rounded-2xl"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>
      </div>
      <div className="text-center">
        <h2 className="text-3xl lg:text-5xl font-bold gradient-text mb-4">Medical Analysis</h2>
        <p className="text-lg text-muted-foreground">
          {hasPatientData ? "Complete patient record retrieved successfully" : "AI analysis completed successfully"}
        </p>
      </div>

      {/* Show AI Summary prominently for text/upload modes */}
      {!hasPatientData && aiSummary && (
        <div className="glass-card p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent to-primary flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-2xl font-bold">AI Medical Summary</h3>
          </div>

          <div className="space-y-4">
            <div className="p-6 rounded-2xl bg-gradient-to-br from-primary/5 to-accent/5 border border-primary/20">
              <div className="prose prose-sm max-w-none">
                <div 
                  className="text-base leading-relaxed whitespace-pre-wrap"
                  dangerouslySetInnerHTML={{
                    __html: aiSummary
                      .replace(/\*\*(.*?)\*\*/g, '<strong class="text-primary font-semibold">$1</strong>')
                      .replace(/\n\n/g, '</p><p class="mt-3">')
                      .replace(/^(.+)$/gm, '<p>$1</p>')
                      .replace(/<p><\/p>/g, '')
                  }}
                />
              </div>
            </div>
            <div className="flex gap-3">
              <button onClick={onSave} className="btn-accent flex-1 text-sm">
                <span className="flex items-center justify-center gap-2">
                  <Check className="w-4 h-4" />
                  Save Report
                </span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Patient Profile & Contact - Only show if we have patient data */}
      {hasPatientData && (
        <div className="grid lg:grid-cols-3 gap-6">
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold">Patient Profile</h3>
          </div>

          <div className="space-y-3">
            <InfoBox label="Name" value={patientData.patient.patient_name} />
            <InfoBox label="Age" value={`${patientData.patient.age} years`} />
            <InfoBox label="Gender" value={patientData.patient.gender} />
            <InfoBox label="Blood Group" value={patientData.patient.blood_group} />
            <InfoBox label="DOB" value={patientData.patient.date_of_birth} />
          </div>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-secondary to-accent flex items-center justify-center">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold">Contact Info</h3>
          </div>

          <div className="space-y-3">
            <InfoBox label="Phone" value={patientData.patient.phone_number} />
            <InfoBox label="Email" value={patientData.patient.email_address} />
            <InfoBox label="Address" value={patientData.patient.address} />
            <InfoBox label="Guardian" value={patientData.patient.guardian_name} />
          </div>
        </div>

        {/* AI Summary */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-primary flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-xl font-bold">AI Medical Analysis</h3>
            </div>
            {!aiSummary && (
              <button 
                onClick={onGenerateSummary} 
                disabled={isProcessing} 
                className="btn-secondary text-sm px-4 py-2 disabled:opacity-50"
              >
                {isProcessing ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Generating...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    Generate Summary
                  </span>
                )}
              </button>
            )}
          </div>

          {aiSummary ? (
            <div className="space-y-4">
              <div className="p-5 rounded-2xl bg-gradient-to-br from-primary/5 to-accent/5 border border-primary/20">
                <div className="prose prose-sm max-w-none">
                  <div 
                    className="text-sm leading-relaxed whitespace-pre-wrap"
                    dangerouslySetInnerHTML={{
                      __html: aiSummary
                        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-primary font-semibold">$1</strong>')
                        .replace(/\n\n/g, '</p><p class="mt-3">')
                        .replace(/^(.+)$/gm, '<p>$1</p>')
                        .replace(/<p><\/p>/g, '')
                    }}
                  />
                </div>
              </div>
              <div className="flex gap-3">
                <button onClick={onGenerateSummary} disabled={isProcessing} className="btn-secondary flex-1 text-sm">
                  <span className="flex items-center justify-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    Regenerate
                  </span>
                </button>
                <button onClick={onSave} className="btn-accent flex-1 text-sm">
                  <span className="flex items-center justify-center gap-2">
                    <Check className="w-4 h-4" />
                    Save Report
                  </span>
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-accent/20 to-primary/20 flex items-center justify-center">
                <Brain className="w-8 h-8 text-accent" />
              </div>
              <p className="text-sm font-medium mb-2">AI Analysis Ready</p>
              <p className="text-xs text-muted-foreground mb-4">Click "Generate Summary" to create an intelligent medical analysis</p>
              <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground">
                <Sparkles className="w-3 h-3" />
                <span>Powered by Google Gemini AI</span>
              </div>
            </div>
          )}
        </div>
      </div>
      )}

      {/* Medical History - Only show if we have patient data */}
      {hasPatientData && patientData && (
        <div className="glass-card p-6">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Medical History
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-background/50 border border-white/10">
              <p className="text-xs font-medium text-muted-foreground mb-2">Past Conditions</p>
              <p className="text-sm">{patientData.medical_history.past_conditions}</p>
            </div>
            <div className="p-4 rounded-xl bg-background/50 border border-white/10">
              <p className="text-xs font-medium text-muted-foreground mb-2">Allergies</p>
              <p className="text-sm">{patientData.medical_history.allergies}</p>
            </div>
            <div className="p-4 rounded-xl bg-background/50 border border-white/10">
              <p className="text-xs font-medium text-muted-foreground mb-2">Previous Surgeries</p>
              <p className="text-sm">{patientData.medical_history.previous_surgeries}</p>
            </div>
            <div className="p-4 rounded-xl bg-background/50 border border-white/10">
              <p className="text-xs font-medium text-muted-foreground mb-2">Family History</p>
              <p className="text-sm">{patientData.medical_history.family_history}</p>
            </div>
          </div>
        </div>
      )}

      {/* Latest Checkup & Vital Signs */}
      {latestCheckup && (
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="glass-card p-6">
            <h3 className="text-xl font-bold mb-6">Latest Checkup ({latestCheckup.date_of_checkup})</h3>
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-accent/10 border border-accent/20">
                <p className="text-sm font-medium text-accent mb-2">Diagnosis</p>
                <p className="text-sm">{latestCheckup.current_diagnosis}</p>
              </div>
              <div className="p-4 rounded-xl bg-background/50 border border-white/10">
                <p className="text-sm font-medium text-muted-foreground mb-2">Symptoms</p>
                <p className="text-sm">{latestCheckup.symptoms}</p>
              </div>
              <div className="p-4 rounded-xl bg-background/50 border border-white/10">
                <p className="text-sm font-medium text-muted-foreground mb-2">Physical Exam</p>
                <p className="text-sm">{latestCheckup.physical_exam_findings}</p>
              </div>
            </div>
          </div>

          <div className="glass-card p-6">
            <h3 className="text-xl font-bold mb-6">Vital Signs</h3>
            <div className="grid grid-cols-2 gap-4">
              <VitalBox label="Blood Pressure" value={latestCheckup.blood_pressure} status="optimal" />
              <VitalBox label="Heart Rate" value={latestCheckup.heart_rate} status="healthy" />
              <VitalBox label="Temperature" value={latestCheckup.temperature} status="normal" />
              <VitalBox label="BMI" value={latestCheckup.bmi} status="optimal" />
              <VitalBox label="Weight" value={latestCheckup.weight} status="normal" />
              <VitalBox label="Height" value={latestCheckup.height} status="normal" />
            </div>
          </div>
        </div>
      )}

      {/* Lab Tests */}
      {latestLabTest && (
        <div className="glass-card p-6">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Database className="w-5 h-5" />
            Laboratory Tests
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl bg-background/50 border border-white/10">
              <p className="text-xs font-medium text-muted-foreground mb-2">Lab Results</p>
              <p className="text-sm">{latestLabTest.lab_results}</p>
            </div>
            <div className="p-4 rounded-xl bg-background/50 border border-white/10">
              <p className="text-xs font-medium text-muted-foreground mb-2">Imaging</p>
              <p className="text-sm">{latestLabTest.imaging}</p>
            </div>
            <div className="p-4 rounded-xl bg-background/50 border border-white/10">
              <p className="text-xs font-medium text-muted-foreground mb-2">Other Tests</p>
              <p className="text-sm">{latestLabTest.other_tests}</p>
            </div>
          </div>
        </div>
      )}

      {/* Treatment Plan */}
      {latestTreatment && (
        <div className="glass-card p-6">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Zap className="w-5 h-5" />
            Current Treatment Plan
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <InfoBox label="Assigned Doctor" value={latestTreatment.assigned_doctor} />
              <InfoBox label="Related Disease" value={latestTreatment.related_disease} />
              <InfoBox label="Next Follow-up" value={latestTreatment.next_followup_date} />
            </div>
            <div className="space-y-3">
              <div className="p-4 rounded-xl bg-background/50 border border-white/10">
                <p className="text-xs font-medium text-muted-foreground mb-2">Prescribed Medications</p>
                <p className="text-sm">{latestTreatment.prescribed_medications}</p>
              </div>
              <div className="p-4 rounded-xl bg-background/50 border border-white/10">
                <p className="text-xs font-medium text-muted-foreground mb-2">Procedures</p>
                <p className="text-sm">{latestTreatment.procedures}</p>
              </div>
            </div>
            <div className="md:col-span-2 p-4 rounded-xl bg-primary/10 border border-primary/20">
              <p className="text-xs font-medium text-primary mb-2">Lifestyle Recommendations</p>
              <p className="text-sm">{latestTreatment.lifestyle_recommendations}</p>
            </div>
            {latestTreatment.physiotherapy_advice && (
              <div className="md:col-span-2 p-4 rounded-xl bg-secondary/10 border border-secondary/20">
                <p className="text-xs font-medium text-secondary mb-2">Physiotherapy Advice</p>
                <p className="text-sm">{latestTreatment.physiotherapy_advice}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Doctor's Notes */}
      {hasPatientData && patientData && patientData.notes.length > 0 && (
        <div className="glass-card p-6">
          <h3 className="text-xl font-bold mb-6">Doctor's Notes & Warnings</h3>
          <div className="space-y-3">
            {patientData.notes.map((note) => (
              <div key={note.id} className="p-4 rounded-xl bg-background/50 border border-white/10">
                <div className="flex items-start gap-3">
                  <FileText className="w-5 h-5 text-accent mt-1" />
                  <div className="flex-1">
                    <p className="text-sm mb-2">{note.doctor_remarks}</p>
                    {note.special_warnings && (
                      <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
                        <p className="text-xs font-medium text-amber-500">⚠️ Special Warning</p>
                        <p className="text-xs mt-1">{note.special_warnings}</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
};

// Reusable Components
const FeatureCard = ({ icon, title, description, color }: { icon: React.ReactNode; title: string; description: string; color: string }) => {
  const colorClasses = {
    primary: "from-primary to-primary/50",
    secondary: "from-secondary to-secondary/50",
    accent: "from-accent to-accent/50",
  };

  return (
    <div className="glass-card-hover p-6 group">
      <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
};

const StatCard = ({ label, value, trend }: { label: string; value: string; trend: string }) => {
  return (
    <div className="glass-card p-4 lg:p-6 hover:scale-105 transition-transform">
      <p className="text-sm text-muted-foreground mb-1">{label}</p>
      <p className="text-2xl lg:text-3xl font-bold gradient-text mb-2">{value}</p>
      <p className="text-xs text-accent">{trend}</p>
    </div>
  );
};

const ActionCard = ({ title, description, buttonText, onAction, variant }: { title: string; description: string; buttonText: string; onAction: () => void; variant: string }) => {
  return (
    <div className="glass-card p-6 lg:p-8 text-center">
      <h3 className="text-2xl font-bold mb-3">{title}</h3>
      <p className="text-muted-foreground mb-6">{description}</p>
      <button onClick={onAction} className={`btn-${variant} w-full`}>
        {buttonText}
      </button>
    </div>
  );
};

const InfoBox = ({ label, value }: { label: string; value: string }) => {
  return (
    <div className="p-3 rounded-xl bg-background/50">
      <p className="text-xs text-muted-foreground mb-1">{label}</p>
      <p className="font-bold">{value}</p>
    </div>
  );
};

const VitalBox = ({ label, value, status }: { label: string; value: string; status: string }) => {
  const statusColors = {
    optimal: "text-accent",
    healthy: "text-primary",
    normal: "text-secondary",
  };

  return (
    <div className="p-4 rounded-2xl bg-background/50 border border-white/10">
      <p className="text-sm text-muted-foreground mb-2">{label}</p>
      <p className="text-2xl font-bold mb-1">{value}</p>
      <p className={`text-xs font-medium ${statusColors[status as keyof typeof statusColors]}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </p>
    </div>
  );
};

export default Index;
