'use client';

import { useState, useEffect } from 'react';
import { Search, Filter, Download, Star, MessageSquare, Clock, CheckCircle, XCircle, AlertCircle, FileText, Eye } from 'lucide-react';

interface Candidate {
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

const mockCandidates: Candidate[] = [
  {
    id: '1',
    name: 'Nguyễn Văn A',
    position: 'Frontend Developer',
    email: 'nguyenvana@email.com',
    phone: '0912345678',
    experience: '3-5',
    appliedDate: '2024-01-15',
    status: 'pending',
    cvUrl: '/cv/nguyenvana.pdf',
    coverLetter: 'Tôi có 3 năm kinh nghiệm phát triển frontend với React và Next.js...',
    skills: ['React', 'TypeScript', 'TailwindCSS', 'Next.js'],
  },
  {
    id: '2',
    name: 'Trần Thị B',
    position: 'Backend Developer',
    email: 'tranthib@email.com',
    phone: '0923456789',
    experience: '1-3',
    appliedDate: '2024-01-14',
    status: 'reviewing',
    score: 75,
    cvUrl: '/cv/tranthib.pdf',
    coverLetter: 'Tôi là backend developer với kinh nghiệm về Node.js và MongoDB...',
    skills: ['Node.js', 'MongoDB', 'Express', 'Docker'],
    notes: 'Có tiềm năng, cần phỏng vấn kỹ thuật',
  },
  {
    id: '3',
    name: 'Lê Văn C',
    position: 'UI/UX Designer',
    email: 'levanc@email.com',
    phone: '0934567890',
    experience: '5+',
    appliedDate: '2024-01-13',
    status: 'accepted',
    score: 90,
    cvUrl: '/cv/levanc.pdf',
    coverLetter: 'Với 5 năm kinh nghiệm thiết kế UI/UX cho các sản phẩm công nghệ...',
    skills: ['Figma', 'Adobe XD', 'Sketch', 'Prototyping'],
    notes: 'Phù hợp hoàn hảo với yêu cầu, đã mời phỏng vấn',
  },
  {
    id: '4',
    name: 'Phạm Thị D',
    position: 'Full Stack Developer',
    email: 'phamthid@email.com',
    phone: '0945678901',
    experience: '0-1',
    appliedDate: '2024-01-12',
    status: 'rejected',
    score: 45,
    cvUrl: '/cv/phamthid.pdf',
    coverLetter: 'Tôi là fresher vừa tốt nghiệp ngành Công nghệ thông tin...',
    skills: ['HTML', 'CSS', 'JavaScript', 'React'],
    notes: 'Chưa đủ kinh nghiệm cho vị trí senior',
  },
];

const statusConfig = {
  pending: { label: 'Chờ duyệt', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
  reviewing: { label: 'Đang xem', color: 'bg-blue-100 text-blue-800', icon: Eye },
  accepted: { label: 'Đồng ý', color: 'bg-green-100 text-green-800', icon: CheckCircle },
  rejected: { label: 'Từ chối', color: 'bg-red-100 text-red-800', icon: XCircle },
};

export default function EvaluatePage() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [positionFilter, setPositionFilter] = useState<string>('all');
  const [showDetails, setShowDetails] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Load candidates from API on component mount
  useEffect(() => {
    loadCandidates();
  }, []);

  const loadCandidates = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('/api/candidates/list');
      if (response.ok) {
        const data = await response.json();
        setCandidates(data);
      } else {
        // Fallback to mock data if API is not available
        setCandidates(mockCandidates);
      }
    } catch (error) {
      console.error('Error loading candidates:', error);
      // Fallback to mock data
      setCandidates(mockCandidates);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredCandidates = candidates.filter(candidate => {
    const matchesSearch = candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         candidate.position.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         candidate.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || candidate.status === statusFilter;
    const matchesPosition = positionFilter === 'all' || candidate.position === positionFilter;
    return matchesSearch && matchesStatus && matchesPosition;
  });

  const updateCandidateStatus = async (candidateId: string, newStatus: Candidate['status']) => {
    try {
      const response = await fetch(`/api/candidates/${candidateId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newStatus),
      });

      if (response.ok) {
        setCandidates(prev => prev.map(c => 
          c.id === candidateId ? { ...c, status: newStatus } : c
        ));
      } else {
        console.error('Failed to update status');
      }
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const updateCandidateScore = async (candidateId: string, score: number) => {
    try {
      const response = await fetch(`/api/candidates/${candidateId}/score`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(score),
      });

      if (response.ok) {
        setCandidates(prev => prev.map(c => 
          c.id === candidateId ? { ...c, score } : c
        ));
      } else {
        console.error('Failed to update score');
      }
    } catch (error) {
      console.error('Error updating score:', error);
    }
  };

  const updateCandidateNotes = async (candidateId: string, notes: string) => {
    try {
      const response = await fetch(`/api/candidates/${candidateId}/notes`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(notes),
      });

      if (response.ok) {
        setCandidates(prev => prev.map(c => 
          c.id === candidateId ? { ...c, notes } : c
        ));
      } else {
        console.error('Failed to update notes');
      }
    } catch (error) {
      console.error('Error updating notes:', error);
    }
  };

  const positions = Array.from(new Set(candidates.map(c => c.position)));

  return (
    <div className="min-h-full" style={{backgroundColor: 'var(--background)', color: 'var(--foreground)'}}>
      <div className="container mx-auto">
        <div className="card" style={{backgroundColor: 'var(--card-bg)', borderColor: 'var(--card-border)'}}>
          <div className="p-responsive" style={{borderColor: 'var(--card-border)', borderBottom: '1px solid'}}>
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
              <div>
                <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">Đánh giá CV</h1>
                <p className="mt-4 text-lg md:text-xl lg:text-2xl font-semibold">
                  Xem và đánh giá hồ sơ ứng viên
                </p>
              </div>
              <div className="flex gap-2">
                <button className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 flex items-center gap-2">
                  <Download className="w-4 h-4" />
                  Xuất báo cáo
                </button>
              </div>
            </div>
          </div>

          <div className="p-responsive" style={{borderColor: 'var(--card-border)', borderBottom: '1px solid'}}>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{color: 'var(--foreground-muted)'}} />
                <input
                  type="text"
                  placeholder="Tìm kiếm ứng viên..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                />
              </div>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
              >
                <option value="all">Tất cả trạng thái</option>
                {Object.entries(statusConfig).map(([key, config]) => (
                  <option key={key} value={key}>{config.label}</option>
                ))}
              </select>

              <select
                value={positionFilter}
                onChange={(e) => setPositionFilter(e.target.value)}
                className="px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
              >
                <option value="all">Tất cả vị trí</option>
                {positions.map(pos => (
                  <option key={pos} value={pos}>{pos}</option>
                ))}
              </select>

              <button className="px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200 flex items-center justify-center gap-2" style={{backgroundColor: 'var(--card-bg)', borderColor: 'var(--card-border)', color: 'var(--foreground)', border: '1px solid'}}>
                <Filter className="w-4 h-4" />
                Bộ lọc
              </button>
            </div>
          </div>

          <div className="divide-y" style={{borderColor: 'var(--card-border)'}}>
            {filteredCandidates.map((candidate) => {
              const StatusIcon = statusConfig[candidate.status].icon;
              return (
                <div key={candidate.id} className="p-responsive transition-colors duration-200" style={{backgroundColor: 'var(--card-bg)'}}>
                  <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
                    <div className="flex-1 w-full">
                      <div className="flex items-center gap-4">
                        <div className="flex-shrink-0">
                          <div className="w-12 h-12 lg:w-14 lg:h-14 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold text-lg lg:text-xl">
                            {candidate.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
                          </div>
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex flex-col sm:flex-row sm:items-center gap-3">
                            <h3 className="text-xl lg:text-2xl font-bold truncate">{candidate.name}</h3>
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusConfig[candidate.status].color}`}>
                              <StatusIcon className="w-3 h-3 mr-1" />
                              {statusConfig[candidate.status].label}
                            </span>
                            {candidate.score && (
                              <div className="flex items-center gap-1">
                                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                                <span className="text-sm font-medium">{candidate.score}/100</span>
                              </div>
                            )}
                          </div>
                          <div className="mt-2 flex items-center gap-4 text-lg text-secondary">
                            <span>{candidate.position}</span>
                            <span>•</span>
                            <span>{candidate.experience} năm kinh nghiệm</span>
                            <span>•</span>
                            <span>Ứng tuyển: {candidate.appliedDate}</span>
                          </div>
                          <div className="mt-2 flex items-center gap-2">
                            <span className="text-lg text-secondary">Kỹ năng:</span>
                            {candidate.skills.map((skill, index) => (
                              <span key={index} className="inline-flex items-center px-3 py-1 rounded-lg text-lg font-semibold" style={{backgroundColor: 'var(--card-bg)', color: 'var(--foreground)', border: '1px solid var(--card-border)'}}>
                                {skill}
                              </span>
                            ))}
                          </div>
                          {candidate.notes && (
                            <div className="mt-3 text-lg text-secondary">
                              <MessageSquare className="inline w-3 h-3 mr-1" />
                              Ghi chú: {candidate.notes}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 ml-4">
                      <button
                        onClick={() => {
                          setSelectedCandidate(candidate);
                          setShowDetails(true);
                        }}
                        className="p-3 rounded-md transition-colors duration-200" style={{color: 'var(--button-primary)'}}
                        title="Xem chi tiết"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => window.open(candidate.cvUrl, '_blank')}
                        className="p-3 rounded-md transition-colors duration-200" style={{color: 'var(--button-primary)'}}
                        title="Xem CV"
                      >
                        <FileText className="w-4 h-4" />
                      </button>
                      <select
                        value={candidate.status}
                        onChange={(e) => updateCandidateStatus(candidate.id, e.target.value as Candidate['status'])}
                        className="px-4 py-2 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                      >
                        {Object.entries(statusConfig).map(([key, config]) => (
                          <option key={key} value={key}>{config.label}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              );
            })}

            {filteredCandidates.length === 0 && (
              <div className="px-6 py-12 text-center">
                <AlertCircle className="mx-auto h-16 w-16" style={{color: 'var(--foreground-muted)'}} />
                <h3 className="mt-4 text-lg font-bold">Không tìm thấy ứng viên</h3>
                <p className="mt-2 text-lg text-secondary">
                  Thử thay đổi điều kiện tìm kiếm hoặc bộ lọc.
                </p>
              </div>
            )}
          </div>
        </div>

        {showDetails && selectedCandidate && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-bold text-gray-900">Chi tiết ứng viên</h2>
                  <button
                    onClick={() => setShowDetails(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <XCircle className="w-6 h-6" />
                  </button>
                </div>
              </div>

              <div className="px-6 py-4 space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Họ tên</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedCandidate.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Vị trí</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedCandidate.position}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Email</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedCandidate.email}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Điện thoại</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedCandidate.phone}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Kinh nghiệm</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedCandidate.experience} năm</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Ngày ứng tuyển</label>
                    <p className="mt-1 text-sm text-gray-900">{selectedCandidate.appliedDate}</p>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Điểm đánh giá</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={selectedCandidate.score || ''}
                      onChange={(e) => {
                        const score = parseInt(e.target.value) || 0;
                        updateCandidateScore(selectedCandidate.id, score);
                        setSelectedCandidate({ ...selectedCandidate, score });
                      }}
                      className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-600">/ 100</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Kỹ năng</label>
                  <div className="flex flex-wrap gap-2">
                    {selectedCandidate.skills.map((skill, index) => (
                      <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Thư giới thiệu</label>
                  <div className="bg-gray-50 p-3 rounded-md">
                    <p className="text-sm text-gray-900">{selectedCandidate.coverLetter}</p>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Ghi chú đánh giá</label>
                  <textarea
                    rows={3}
                    value={selectedCandidate.notes || ''}
                    onChange={(e) => {
                      updateCandidateNotes(selectedCandidate.id, e.target.value);
                      setSelectedCandidate({ ...selectedCandidate, notes: e.target.value });
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Nhập ghi chú về ứng viên..."
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t">
                  <button
                    onClick={() => window.open(selectedCandidate.cvUrl, '_blank')}
                    className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 flex items-center gap-2"
                  >
                    <FileText className="w-4 h-4" />
                    Xem CV
                  </button>
                  <button
                    onClick={() => setShowDetails(false)}
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                  >
                    Đóng
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
