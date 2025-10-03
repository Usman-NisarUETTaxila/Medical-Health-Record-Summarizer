import { useState } from "react";
import { Brain, Sparkles, Shield, Zap, Upload, Database, FileText, Home, ArrowRight, Check, Loader2 } from "lucide-react";
import { toast } from "@/hooks/use-toast";

interface PatientData {
  id: string;
  name: string;
  age: number;
  gender: string;
  bloodType: string;
  diagnosis: string;
  symptoms: string;
  vitalSigns: {
    bloodPressure: string;
    heartRate: string;
    temperature: string;
  };
}

type WorkflowStep = "home" | "input" | "processing" | "results";
type InputMode = "database" | "upload" | "text";

const Index = () => {
  const [currentStep, setCurrentStep] = useState<WorkflowStep>("home");
  const [inputMode, setInputMode] = useState<InputMode>("database");
  const [patientId, setPatientId] = useState("");
  const [textInput, setTextInput] = useState("");
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
    if (inputMode === "database" && !patientId.trim()) {
      toast({
        title: "Patient ID required",
        description: "Please enter a patient ID",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    setCurrentStep("processing");

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2500));

    const mockData: PatientData = {
      id: patientId || `PAT-${Date.now()}`,
      name: "Dr. Sarah Chen",
      age: 34,
      gender: "Female",
      bloodType: "A+",
      diagnosis: "Excellent health status, continue preventive care",
      symptoms: "Routine health screening, no acute symptoms",
      vitalSigns: {
        bloodPressure: "118/75",
        heartRate: "68 bpm",
        temperature: "98.2°F",
      },
    };

    setPatientData(mockData);
    setIsProcessing(false);
    setCurrentStep("results");

    toast({
      title: "Data retrieved successfully",
      description: "AI analysis is ready",
    });
  };

  const handleGenerateSummary = async () => {
    setIsProcessing(true);

    // Simulate AI processing
    await new Promise((resolve) => setTimeout(resolve, 3000));

    const summary = `🧠 AI MEDICAL ANALYSIS REPORT

**Patient**: ${patientData?.name} | ${patientData?.age}y ${patientData?.gender}
**Blood Type**: ${patientData?.bloodType}

**Current Assessment**: ${patientData?.diagnosis}

**Vital Signs Analysis**:
• Blood Pressure: ${patientData?.vitalSigns.bloodPressure} - Optimal
• Heart Rate: ${patientData?.vitalSigns.heartRate} - Healthy range
• Temperature: ${patientData?.vitalSigns.temperature} - Normal

**AI Recommendations**:
✓ Continue current wellness protocol
✓ Regular preventive screenings advised
✓ Lifestyle optimization suggestions available

**Confidence Score**: 97.3% | Analysis completed`;

    setAiSummary(summary);
    setIsProcessing(false);

    toast({
      title: "AI analysis complete",
      description: "Medical summary has been generated",
    });
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
            onFetch={handleFetchData}
            isProcessing={isProcessing}
          />
        )}
        {currentStep === "processing" && <ProcessingPage />}
        {currentStep === "results" && (
          <ResultsPage
            patientData={patientData}
            aiSummary={aiSummary}
            onGenerateSummary={handleGenerateSummary}
            onSave={handleSaveData}
            isProcessing={isProcessing}
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
  onFetch,
  isProcessing,
}: {
  inputMode: InputMode;
  setInputMode: (mode: InputMode) => void;
  patientId: string;
  setPatientId: (id: string) => void;
  textInput: string;
  setTextInput: (text: string) => void;
  onFetch: () => void;
  isProcessing: boolean;
}) => {
  const inputModes = [
    { id: "database" as InputMode, name: "Database", icon: Database, description: "Retrieve existing patient records" },
    { id: "upload" as InputMode, name: "Upload", icon: Upload, description: "Upload medical documents" },
    { id: "text" as InputMode, name: "Text", icon: FileText, description: "Paste medical report text" },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in-up">
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
          <div className="border-2 border-dashed border-white/20 rounded-3xl p-12 text-center hover:border-primary/50 transition-all cursor-pointer">
            <Upload className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
            <p className="font-medium mb-2">Drop files here or click to browse</p>
            <p className="text-sm text-muted-foreground">Supports: PDF, JPG, PNG, DICOM</p>
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
              Fetch Data
              <ArrowRight className="w-5 h-5" />
            </span>
          )}
        </button>
      </div>
    </div>
  );
};

// Processing Page
const ProcessingPage = () => {
  return (
    <div className="flex items-center justify-center min-h-[60vh] animate-scale-in">
      <div className="text-center">
        <div className="w-24 h-24 lg:w-32 lg:h-32 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center mx-auto mb-8 animate-glow-pulse">
          <Loader2 className="w-12 h-12 lg:w-16 lg:h-16 text-white animate-spin" />
        </div>
        <h2 className="text-3xl lg:text-4xl font-bold gradient-text mb-4">AI Processing Data</h2>
        <p className="text-lg text-muted-foreground">Analyzing medical information...</p>
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
}: {
  patientData: PatientData | null;
  aiSummary: string;
  onGenerateSummary: () => void;
  onSave: () => void;
  isProcessing: boolean;
}) => {
  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-fade-in-up">
      <div className="text-center">
        <h2 className="text-3xl lg:text-5xl font-bold gradient-text mb-4">Medical Analysis</h2>
        <p className="text-lg text-muted-foreground">Patient data retrieved successfully</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Patient Profile */}
        {patientData && (
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-xl font-bold">Patient Profile</h3>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <InfoBox label="Name" value={patientData.name} />
              <InfoBox label="Age" value={`${patientData.age} years`} />
              <InfoBox label="Gender" value={patientData.gender} />
              <InfoBox label="Blood Type" value={patientData.bloodType} />
            </div>

            <div className="p-4 rounded-2xl bg-accent/10 border border-accent/20">
              <p className="text-sm font-medium text-accent mb-2">Diagnosis</p>
              <p className="text-sm">{patientData.diagnosis}</p>
            </div>
          </div>
        )}

        {/* AI Summary */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-secondary to-accent flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold">AI Analysis</h3>
          </div>

          {aiSummary ? (
            <div className="p-4 rounded-2xl bg-background/50 border border-white/10 max-h-96 overflow-y-auto">
              <pre className="text-sm whitespace-pre-wrap font-mono">{aiSummary}</pre>
            </div>
          ) : (
            <div className="text-center py-12">
              <Brain className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
              <p className="font-medium mb-2">Ready for AI Analysis</p>
              <p className="text-sm text-muted-foreground">Generate comprehensive medical summary</p>
            </div>
          )}
        </div>
      </div>

      {/* Vital Signs */}
      {patientData && (
        <div className="glass-card p-6">
          <h3 className="text-xl font-bold mb-6">Vital Signs</h3>
          <div className="grid sm:grid-cols-3 gap-4">
            <VitalBox label="Blood Pressure" value={patientData.vitalSigns.bloodPressure} status="optimal" />
            <VitalBox label="Heart Rate" value={patientData.vitalSigns.heartRate} status="healthy" />
            <VitalBox label="Temperature" value={patientData.vitalSigns.temperature} status="normal" />
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-4">
        {!aiSummary ? (
          <button onClick={onGenerateSummary} disabled={isProcessing} className="btn-secondary flex-1 disabled:opacity-50">
            {isProcessing ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating...
              </span>
            ) : (
              "Generate Summary"
            )}
          </button>
        ) : (
          <button onClick={onSave} className="btn-accent flex-1">
            <span className="flex items-center justify-center gap-2">
              <Check className="w-5 h-5" />
              Save to Database
            </span>
          </button>
        )}
      </div>
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
