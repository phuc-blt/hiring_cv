const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface JDRequest {
  jobTitle: string;
  department: string;
  location: string;
  jobType: string;
  experience: string;
  salary?: string;
  description: string;
  requirements: string[];
  benefits?: string[];
  platforms: string[];
}

export interface ApplicationRequest {
  fullName: string;
  email: string;
  phone: string;
  address: string;
  position: string;
  experience: string;
  coverLetter: string;
  portfolio?: string;
  expectedSalary?: string;
  availability: string;
  cvFile: File;
}

export interface CVParseRequest {
  cv_content: string;
  jd_text?: string;
  role?: string;
  company_context?: string;
}

export interface Candidate {
  id: string;
  name: string;
  position: string;
  email: string;
  phone: string;
  experience: string;
  appliedDate: string;
  status: 'pending' | 'reviewing' | 'accepted' | 'rejected';
  score?: number;
  cvUrl: string;
  coverLetter: string;
  skills: string[];
  notes?: string;
}

class APIService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // JD Creation and Posting
  async createJD(jdRequest: JDRequest) {
    return this.request('/api/jd/create', {
      method: 'POST',
      body: JSON.stringify(jdRequest),
    });
  }

  async listJDs() {
    return this.request('/api/jd/list');
  }

  // Application Submission
  async submitApplication(applicationData: ApplicationRequest) {
    const formData = new FormData();
    
    // Add all form fields
    Object.keys(applicationData).forEach(key => {
      if (key === 'cvFile') {
        formData.append('cvFile', applicationData[key]);
      } else if (applicationData[key as keyof ApplicationRequest] !== undefined) {
        formData.append(key, String(applicationData[key as keyof ApplicationRequest]));
      }
    });

    return this.request('/api/apply/submit', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  }

  async listApplications() {
    return this.request('/api/applications/list');
  }

  // CV Evaluation
  async evaluateCV(request: CVParseRequest) {
    return this.request('/api/evaluate/cv', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async evaluateCVFile(
    cvFile: File,
    jdText?: string,
    role?: string,
    companyContext?: string
  ) {
    const formData = new FormData();
    formData.append('cvFile', cvFile);
    
    if (jdText) formData.append('jd_text', jdText);
    if (role) formData.append('role', role);
    if (companyContext) formData.append('company_context', companyContext);

    return this.request('/api/evaluate/cv-file', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  }

  // Candidate Management
  async listCandidates(): Promise<Candidate[]> {
    return this.request('/api/candidates/list');
  }

  async updateCandidateStatus(candidateId: string, status: string) {
    return this.request(`/api/candidates/${candidateId}/status`, {
      method: 'PUT',
      body: JSON.stringify(status),
    });
  }

  async updateCandidateScore(candidateId: string, score: number) {
    return this.request(`/api/candidates/${candidateId}/score`, {
      method: 'PUT',
      body: JSON.stringify(score),
    });
  }

  async updateCandidateNotes(candidateId: string, notes: string) {
    return this.request(`/api/candidates/${candidateId}/notes`, {
      method: 'PUT',
      body: JSON.stringify(notes),
    });
  }

  // Interview Kit Generation
  async generateInterviewKit(candidateId: string) {
    return this.request('/api/interview/generate-kit', {
      method: 'POST',
      body: JSON.stringify({ candidate_id: candidateId }),
    });
  }

  // Health Check
  async healthCheck() {
    return this.request('/api/health');
  }
}

export const apiService = new APIService();

// Helper functions for common operations
export const jdAPI = {
  create: (data: JDRequest) => apiService.createJD(data),
  list: () => apiService.listJDs(),
};

export const applicationAPI = {
  submit: (data: ApplicationRequest) => apiService.submitApplication(data),
  list: () => apiService.listApplications(),
};

export const evaluationAPI = {
  evaluateCV: (request: CVParseRequest) => apiService.evaluateCV(request),
  evaluateFile: (file: File, jdText?: string, role?: string, companyContext?: string) => 
    apiService.evaluateCVFile(file, jdText, role, companyContext),
  listCandidates: () => apiService.listCandidates(),
  updateStatus: (id: string, status: string) => apiService.updateCandidateStatus(id, status),
  updateScore: (id: string, score: number) => apiService.updateCandidateScore(id, score),
  updateNotes: (id: string, notes: string) => apiService.updateCandidateNotes(id, notes),
};

export const interviewAPI = {
  generateKit: (candidateId: string) => apiService.generateInterviewKit(candidateId),
};

export default apiService;
