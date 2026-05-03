# Hiring CV System API Documentation

## Overview
API để kết nối frontend với các AI agents trong hệ thống tuyển dụng và đánh giá CV.

## Backend Setup

### Cài đặt dependencies
```bash
pip install fastapi uvicorn python-multipart
```

### Khởi động server
```bash
cd /workspace/phucnt/hiring_CV
python -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. Job Description (JD) Management

#### Tạo JD và đăng tuyển
```
POST /api/jd/create
```

**Request Body:**
```json
{
  "jobTitle": "Frontend Developer",
  "department": "Technology", 
  "location": "Hanoi",
  "jobType": "full-time",
  "experience": "mid",
  "salary": "20-30 million VND",
  "description": "We are looking for a skilled frontend developer...",
  "requirements": ["React", "TypeScript", "3+ years experience"],
  "benefits": ["Health insurance", "Flexible working hours"],
  "platforms": ["linkedin", "indeed", "topcv"]
}
```

**Response:**
```json
{
  "success": true,
  "jd_id": "jd_20240102_123456",
  "jd_data": {...},
  "enhanced_jd": "AI-enhanced job description...",
  "posting_results": {
    "linkedin": {"status": "pending", "message": "Will be posted to LinkedIn"},
    "indeed": {"status": "pending", "message": "Will be posted to Indeed"}
  },
  "message": "Job description created successfully and ready for posting"
}
```

#### Lấy danh sách JD
```
GET /api/jd/list
```

### 2. Application Submission

#### Nộp hồ sơ ứng tuyển
```
POST /api/apply/submit
```

**Request (FormData):**
- `fullName`: Họ và tên
- `email`: Email
- `phone`: Điện thoại
- `address`: Địa chỉ
- `position`: Vị trí ứng tuyển
- `experience`: Kinh nghiệm
- `coverLetter`: Thư giới thiệu
- `portfolio`: Portfolio (optional)
- `expectedSalary`: Mức lương mong muốn (optional)
- `availability`: Thời gian có thể bắt đầu
- `cvFile`: File CV (PDF, DOC, DOCX)

**Response:**
```json
{
  "success": true,
  "application_id": "app_20240102_123456",
  "message": "Application submitted successfully",
  "status": "pending_evaluation"
}
```

#### Lấy danh sách applications
```
GET /api/applications/list
```

### 3. CV Evaluation

#### Đánh giá CV (text)
```
POST /api/evaluate/cv
```

**Request Body:**
```json
{
  "cv_content": "CV text content...",
  "jd_text": "Job description text...",
  "role": "Frontend Developer",
  "company_context": "Technology company context..."
}
```

**Response:**
```json
{
  "skills_analysis": {...},
  "projects_analysis": {...},
  "scoring": {...},
  "retrieval": {...},
  "comprehensive_report": "Detailed evaluation report...",
  "executive_summary": "Summary of evaluation...",
  "jd_text": "Job description used for evaluation"
}
```

#### Đánh giá CV (file upload)
```
POST /api/evaluate/cv-file
```

**Request (FormData):**
- `cvFile`: File CV
- `jd_text`: Job description (optional)
- `role`: Vị trí (optional)
- `company_context`: Context công ty (optional)

### 4. Candidate Management

#### Lấy danh sách ứng viên
```
GET /api/candidates/list
```

**Response:**
```json
[
  {
    "id": "app_20240102_123456",
    "name": "John Doe",
    "position": "Frontend Developer",
    "email": "john@example.com",
    "phone": "0912345678",
    "experience": "3-5",
    "appliedDate": "2024-01-02",
    "status": "pending",
    "score": 75,
    "cvUrl": "uploads/cv_20240102_123456_john_cv.pdf",
    "coverLetter": "Cover letter text...",
    "skills": ["React", "TypeScript", "Node.js"],
    "notes": "Good candidate, needs technical interview"
  }
]
```

#### Cập nhật trạng thái ứng viên
```
PUT /api/candidates/{candidate_id}/status
```

**Request Body:** `"pending"` | `"reviewing"` | `"accepted"` | `"rejected"`

#### Cập nhật điểm ứng viên
```
PUT /api/candidates/{candidate_id}/score
```

**Request Body:** `85` (0-100)

#### Cập nhật ghi chú
```
PUT /api/candidates/{candidate_id}/notes
```

**Request Body:** `"Candidate notes..."`

### 5. Interview Kit Generation

#### Tạo bộ phỏng vấn
```
POST /api/interview/generate-kit
```

**Request Body:**
```json
{
  "candidate_id": "app_20240102_123456"
}
```

**Response:**
```json
{
  "success": true,
  "candidate_id": "app_20240102_123456",
  "interview_kit": {
    "candidate_profile": {...},
    "interview_questions": [...],
    "feedback_points": [...]
  }
}
```

### 6. Health Check

#### Kiểm tra trạng thái API
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-02T12:34:56.789Z",
  "version": "1.0.0"
}
```

## Frontend Integration

### API Client Service
Frontend đã được tích hợp với API thông qua:

1. **API Service** (`/frontend/app/services/api.ts`)
   - Các hàm wrapper cho tất cả API endpoints
   - Error handling và response parsing
   - TypeScript interfaces cho type safety

2. **Next.js API Routes** (Proxy đến backend)
   - `/frontend/app/api/jd/create/route.ts`
   - `/frontend/app/api/apply/submit/route.ts`
   - `/frontend/app/api/candidates/list/route.ts`
   - `/frontend/app/api/candidates/[id]/status/route.ts`
   - `/frontend/app/api/candidates/[id]/score/route.ts`
   - `/frontend/app/api/candidates/[id]/notes/route.ts`

3. **Component Integration**
   - JDForm component → `/api/jd/create`
   - Apply page → `/api/apply/submit`
   - Evaluate page → `/api/candidates/*`

### Environment Variables
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (environment)
BACKEND_URL=http://localhost:8000
```

## AI Agents Integration

API kết nối với các AI agents sau:

1. **JDAgent** - Tạo và tối ưu Job Description
2. **SkillAgent** - Trích xuất kỹ năng từ CV
3. **ProjectAgent** - Phân tích dự án
4. **ScoringAgent** - Chấm điểm ứng viên
5. **RetrievalAgent** - RAG retrieval
6. **ReportAgent** - Tạo báo cáo và interview kit
7. **OrchestratorAgent** - Điều phối các agents

## Error Handling

API trả về các HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `404` - Not Found  
- `500` - Internal Server Error

Error response format:
```json
{
  "error": "Error message description"
}
```

## Testing

### Test API endpoints
```bash
cd /workspace/phucnt/hiring_CV
python test_api.py
```

### Test frontend integration
1. Khởi động backend: `python -m uvicorn app.api:app --port 8000`
2. Khởi động frontend: `cd frontend && npm run dev`
3. Truy cập http://localhost:3000

## Production Considerations

1. **Database**: Thay thế in-memory storage với PostgreSQL/MongoDB
2. **File Storage**: Sử dụng AWS S3 hoặc similar cho CV files
3. **Authentication**: Thêm JWT authentication
4. **Rate Limiting**: Implement rate limiting
5. **Logging**: Structured logging với ELK stack
6. **Monitoring**: Health checks và metrics
7. **Security**: Input validation và sanitization
