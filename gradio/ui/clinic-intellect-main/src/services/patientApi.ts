import { PatientData } from "@/types/patient";

const API_BASE_URL = 'http://localhost:8000/patient-app'; // Update with your actual API base URL

export const fetchPatientById = async (patientId: string): Promise<PatientData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/patients/${patientId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Add any required authentication headers here
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch patient data');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching patient data:', error);
    throw error;
  }
};

export const generateAISummary = async (patientId: number): Promise<string> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/patients/${patientId}/summary/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to generate AI summary');
    }

    const data = await response.json();
    return data.summary;
  } catch (error) {
    console.error('Error generating AI summary:', error);
    throw error;
  }
};

export const generateSummaryFromText = async (text: string): Promise<string> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/summary/text/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to generate summary from text');
    }

    const data = await response.json();
    return data.summary;
  } catch (error) {
    console.error('Error generating summary from text:', error);
    throw error;
  }
};

export const generateSummaryFromFile = async (file: File): Promise<string> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/summary/file/`, {
      method: 'POST',
      body: formData,
      // Don't set Content-Type header - browser will set it with boundary for multipart/form-data
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || errorData.details || 'Failed to generate summary from file');
    }

    const data = await response.json();
    return data.summary;
  } catch (error) {
    console.error('Error generating summary from file:', error);
    throw error;
  }
};
