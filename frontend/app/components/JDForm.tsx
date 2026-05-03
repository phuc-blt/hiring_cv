'use client';

import { useState, Fragment } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Save, Send, Plus, Trash2, FileText, Building, MapPin, DollarSign, Briefcase, Users, Target, Loader2 } from 'lucide-react';

const jdSchema = z.object({
  jobTitle: z.string().min(1, 'Vui lòng nhập vị trí tuyển dụng'),
  department: z.string().min(1, 'Vui lòng nhập phòng ban'),
  location: z.string().min(1, 'Vui lòng nhập địa điểm làm việc'),
  jobType: z.enum(['full-time', 'part-time', 'contract', 'internship']),
  experience: z.enum(['entry', 'junior', 'mid', 'senior', 'lead']),
  salary: z.string().optional(),
  description: z.string().min(10, 'Mô tả công việc phải có ít nhất 10 ký tự'),
  requirements: z.array(z.string()).min(1, 'Vui lòng thêm ít nhất một yêu cầu'),
  benefits: z.array(z.string()).optional(),
  platforms: z.array(z.string()).min(1, 'Vui lòng chọn ít nhất một nền tảng'),
});

type JDFormData = z.infer<typeof jdSchema>;

const platforms = [
  { id: 'linkedin', label: 'LinkedIn' },
  { id: 'indeed', label: 'Indeed' },
  { id: 'vietnamworks', label: 'VietnamWorks' },
  { id: 'topcv', label: 'TopCV' },
  { id: 'careerbuilder', label: 'CareerBuilder' },
];

const jobTypes = [
  { value: 'full-time', label: 'Toàn thời gian' },
  { value: 'part-time', label: 'Bán thời gian' },
  { value: 'contract', label: 'Hợp đồng' },
  { value: 'internship', label: 'Thực tập' },
];

const experienceLevels = [
  { value: 'entry', label: 'Mới vào nghề' },
  { value: 'junior', label: 'Junior (1-2 năm)' },
  { value: 'mid', label: 'Mid-level (3-5 năm)' },
  { value: 'senior', label: 'Senior (5+ năm)' },
  { value: 'lead', label: 'Lead/Manager' },
];

export default function JDForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [requirementInput, setRequirementInput] = useState('');
  const [benefitInput, setBenefitInput] = useState('');
  const [generatedJD, setGeneratedJD] = useState<any>(null);
  const [showPreview, setShowPreview] = useState(false);
  const [editableJD, setEditableJD] = useState<any>(null);
  const [previewPlatforms, setPreviewPlatforms] = useState<string[]>([]);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<JDFormData>({
    resolver: zodResolver(jdSchema),
    defaultValues: {
      jobTitle: '',
      department: '',
      location: '',
      jobType: 'full-time',
      experience: 'mid',
      salary: '',
      description: '',
      requirements: [],
      benefits: [],
      platforms: [],
    },
  });

  const requirements = watch('requirements') || [];
  const benefits = watch('benefits') || [];
  const selectedPlatforms = watch('platforms') || [];

  const addRequirement = () => {
    if (requirementInput.trim()) {
      const currentRequirements = watch('requirements') || [];
      setValue('requirements', [...currentRequirements, requirementInput.trim()]);
      setRequirementInput('');
    }
  };

  const removeRequirement = (index: number) => {
    const currentRequirements = watch('requirements') || [];
    setValue('requirements', currentRequirements.filter((_, i) => i !== index));
  };

  const addBenefit = () => {
    if (benefitInput.trim()) {
      const currentBenefits = watch('benefits') || [];
      setValue('benefits', [...currentBenefits, benefitInput.trim()]);
      setBenefitInput('');
    }
  };

  const removeBenefit = (index: number) => {
    const currentBenefits = watch('benefits') || [];
    setValue('benefits', currentBenefits.filter((_, i) => i !== index));
  };

  const togglePlatform = (platformId: string) => {
    const currentPlatforms = watch('platforms') || [];
    const newPlatforms = currentPlatforms.includes(platformId)
      ? currentPlatforms.filter(p => p !== platformId)
      : [...currentPlatforms, platformId];
    setValue('platforms', newPlatforms);
  };

  const handleCreateJD = async () => {
    console.log('=== CREATE JD START ===');
    
    // Get current form values
    const currentValues = watch();
    console.log('Current form values:', currentValues);
    console.log('Form errors:', errors);
    
    // Debug each field
    console.log('=== DETAILED DEBUG ===');
    console.log('currentValues:', currentValues);
    console.log('jobTitle:', currentValues.jobTitle);
    console.log('department:', currentValues.department);
    console.log('location:', currentValues.location);
    console.log('jobType:', currentValues.jobType);
    console.log('experience:', currentValues.experience);
    console.log('description:', currentValues.description);
    console.log('requirements from currentValues:', currentValues.requirements);
    console.log('platforms from currentValues:', currentValues.platforms);
    console.log('requirements from watch:', requirements);
    console.log('platforms from watch:', selectedPlatforms);
    console.log('requirements length:', requirements?.length);
    console.log('platforms length:', selectedPlatforms?.length);
    console.log('requirements type:', typeof requirements);
    console.log('platforms type:', typeof selectedPlatforms);
    console.log('requirementInput:', requirementInput);
    console.log('addRequirement function exists:', typeof addRequirement);
    console.log('=== END DEBUG ===');
    
    // Validate manually - be more specific about what's missing
    const missingFields = [];
    if (!currentValues.jobTitle) missingFields.push('jobTitle');
    if (!currentValues.department) missingFields.push('department');
    if (!currentValues.location) missingFields.push('location');
    if (!currentValues.jobType) missingFields.push('jobType');
    if (!currentValues.experience) missingFields.push('experience');
    if (!currentValues.description) missingFields.push('description');
    if (!requirements || requirements.length === 0) missingFields.push('requirements');
    if (!selectedPlatforms || selectedPlatforms.length === 0) missingFields.push('platforms');
    
    if (missingFields.length > 0) {
      console.error('Validation failed. Missing fields:', missingFields);
      alert(`Vui lòng điền đầy đủ các trường bắt buộc: ${missingFields.join(', ')}`);
      return;
    }
    
    setIsSubmitting(true);
    try {
      const jdRequest = {
        jobTitle: currentValues.jobTitle,
        department: currentValues.department,
        location: currentValues.location,
        jobType: currentValues.jobType,
        experience: currentValues.experience,
        salary: currentValues.salary,
        description: currentValues.description,
        requirements: requirements,
        benefits: currentValues.benefits,
        platforms: selectedPlatforms,
      };

      console.log('Sending request to API:', jdRequest);

      console.log('Sending request to API:', jdRequest);
      
      const response = await fetch('http://localhost:8000/api/jd/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jdRequest),
      });

      console.log('API response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API error response:', errorText);
        throw new Error(`Failed to create JD: ${response.status} ${errorText}`);
      }

      const result = await response.json();
      console.log('JD created successfully:', result);
      
      // Set the generated JD with original form data + enhanced JD
      setGeneratedJD({
        ...result,
        jobTitle: currentValues.jobTitle,
        department: currentValues.department,
        location: currentValues.location,
        jobType: currentValues.jobType,
        experience: currentValues.experience,
        salary: currentValues.salary,
        description: currentValues.description,
        requirements: requirements,
        benefits: currentValues.benefits,
        platforms: selectedPlatforms,
      });
      setEditableJD({
        ...result,
        jobTitle: currentValues.jobTitle,
        department: currentValues.department,
        location: currentValues.location,
        jobType: currentValues.jobType,
        experience: currentValues.experience,
        salary: currentValues.salary,
        description: currentValues.description,
        requirements: requirements,
        benefits: currentValues.benefits,
        platforms: selectedPlatforms,
      });
      setPreviewPlatforms(selectedPlatforms || []);
      setShowPreview(true);
      
      alert('JD đã được tạo thành công! Vui lòng xem và chỉnh sửa trước khi đăng.');
      
    } catch (error) {
      console.error('Error submitting JD:', error);
      alert(`Có lỗi xảy ra: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsSubmitting(false);
      console.log('=== CREATE JD END ===');
    }
  };

  const handleConfirmPost = async () => {
    if (!generatedJD || !generatedJD.id) {
      alert('Không tìm thấy JD để đăng!');
      return;
    }

    setIsSubmitting(true);
    try {
      console.log('Posting JD with ID:', generatedJD.id);
      console.log('Selected platforms:', previewPlatforms);
      
      const response = await fetch(`http://localhost:8000/api/jd/${generatedJD.id}/post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Post API response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Post API error:', errorText);
        throw new Error(`Failed to post JD: ${response.status}`);
      }

      const result = await response.json();
      console.log('JD posted successfully:', result);
      
      alert(`JD đã được đăng thành công lên các nền tảng: ${previewPlatforms.join(', ')}!`);
      setShowPreview(false);
      setGeneratedJD(null);
      setEditableJD(null);
      
      // Reset form
      window.location.reload();
      
    } catch (error) {
      console.error('Error posting JD:', error);
      alert(`Có lỗi xảy ra khi đăng JD: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Fragment>
      <form className="space-y-8" noValidate>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-3">
          <label className="block text-lg font-bold mb-3 flex items-center">
            <FileText className="w-5 h-5 mr-2" style={{color: 'var(--button-primary)'}} />
            Vị trí tuyển dụng *
          </label>
          <input
            {...register('jobTitle')}
            className="w-full text-lg font-semibold transition-all duration-300" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
            placeholder="Ví dụ: Senior Frontend Developer"
          />
          {errors.jobTitle && (
            <p className="mt-2 text-lg font-semibold text-red-400 slide-in">{String(errors.jobTitle.message)}</p>
          )}
        </div>

        <div className="space-y-3">
          <label className="block text-lg font-bold mb-3 flex items-center">
            <Building className="w-5 h-5 mr-2" style={{color: 'var(--button-primary)'}} />
            Phòng ban *
          </label>
          <input
            {...register('department')}
            className="w-full text-lg font-semibold transition-all duration-300" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
            placeholder="Ví dụ: Technology"
          />
          {errors.department && (
            <p className="mt-2 text-lg font-semibold text-red-400 slide-in">{String(errors.department.message)}</p>
          )}
        </div>

        <div className="space-y-3">
          <label className="block text-lg font-bold mb-3 flex items-center">
            <MapPin className="w-5 h-5 mr-2" style={{color: 'var(--button-primary)'}} />
            Địa điểm làm việc *
          </label>
          <input
            {...register('location')}
            className="w-full text-lg font-semibold transition-all duration-300" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
            placeholder="Ví dụ: Hà Nội, TP.HCM"
          />
          {errors.location && (
            <p className="mt-2 text-lg font-semibold text-red-400 slide-in">{String(errors.location.message)}</p>
          )}
        </div>

        <div className="space-y-3">
          <label className="block text-lg font-bold mb-2 flex items-center">
            <DollarSign className="w-5 h-5 mr-2" style={{color: 'var(--button-primary)'}} />
            Mức lương
          </label>
          <input
            {...register('salary')}
            className="w-full text-lg font-semibold transition-all duration-300" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
            placeholder="Ví dụ: 20-30 triệu VNĐ"
          />
        </div>

        <div>
          <label className="block text-lg font-bold mb-2">
            Loại hình công việc *
          </label>
          <select
            {...register('jobType')}
            onChange={(e) => {
              setValue('jobType', e.target.value as any);
            }}
            className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
          >
            <option value="">Chọn loại hình</option>
            {jobTypes.map(type => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
          {errors.jobType && (
            <p className="mt-2 text-lg font-semibold text-red-400">{String(errors.jobType.message)}</p>
          )}
        </div>

        <div>
          <label className="block text-lg font-bold mb-2">
            Kinh nghiệm *
          </label>
          <select
            {...register('experience')}
            onChange={(e) => {
              setValue('experience', e.target.value as any);
            }}
            className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
          >
            <option value="">Chọn kinh nghiệm</option>
            {experienceLevels.map(level => (
              <option key={level.value} value={level.value}>
                {level.label}
              </option>
            ))}
          </select>
          {errors.experience && (
            <p className="mt-2 text-lg font-semibold text-red-400">{String(errors.experience.message)}</p>
          )}
        </div>
      </div>

      <div>
        <label className="block text-lg font-bold mb-2">
          Mô tả công việc *
        </label>
        <textarea
          {...register('description')}
          rows={6}
          className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
          style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
          placeholder="Mô tả chi tiết về công việc, trách nhiệm..."
        />
        {errors.description && (
          <p className="mt-2 text-lg font-semibold text-red-400">{String(errors.description.message)}</p>
        )}
      </div>

      <div>
        <label className="block text-lg font-bold mb-2">
          Yêu cầu công việc *
        </label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={requirementInput}
            onChange={(e) => setRequirementInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addRequirement())}
            className="flex-1 px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
            placeholder="Nhập yêu cầu và nhấn Enter hoặc Thêm"
          />
          <button
            type="button"
            onClick={addRequirement}
            className="px-6 py-3 btn-primary flex items-center gap-2"
            style={{color: 'var(--foreground)'}}
          >
            <Plus className="w-4 h-4" />
            Thêm
          </button>
        </div>
        <div className="space-y-2">
          {requirements.map((req, index) => (
            <div key={index} className="flex items-center justify-between p-3 rounded" 
                 style={{backgroundColor: 'var(--card-bg)', borderColor: 'var(--card-border)', border: '1px solid'}}>
              <span className="text-lg">{req}</span>
              <button
                type="button"
                onClick={() => removeRequirement(index)}
                className="rounded-md transition-colors duration-200" 
                style={{color: 'var(--button-primary)'}}
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
        {errors.requirements && (
          <p className="mt-2 text-lg font-semibold text-red-400">{String(errors.requirements.message)}</p>
        )}
      </div>

      <div>
        <label className="block text-lg font-bold mb-2">
          Quyền lợi (không bắt buộc)
        </label>
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={benefitInput}
            onChange={(e) => setBenefitInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addBenefit())}
            className="flex-1 px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
            style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
            placeholder="Nhập quyền lợi và nhấn Enter hoặc Thêm"
          />
          <button
            type="button"
            onClick={addBenefit}
            className="px-6 py-3 btn-primary flex items-center gap-2"
            style={{color: 'var(--foreground)'}}
          >
            <Plus className="w-4 h-4" />
            Thêm
          </button>
        </div>
        <div className="space-y-2">
          {benefits.map((benefit, index) => (
            <div key={index} className="flex items-center justify-between p-3 rounded" 
                 style={{backgroundColor: 'var(--card-bg)', borderColor: 'var(--card-border)', border: '1px solid'}}>
              <span className="text-lg">{benefit}</span>
              <button
                type="button"
                onClick={() => removeBenefit(index)}
                className="rounded-md transition-colors duration-200" 
                style={{color: 'var(--button-primary)'}}
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-lg font-bold mb-2">
          Nền tảng đăng tuyển *
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {platforms.map(platform => (
            <label key={platform.id} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={selectedPlatforms.includes(platform.id)}
                onChange={() => togglePlatform(platform.id)}
                className="w-5 h-5 rounded focus:ring-2"
                style={{accentColor: 'var(--button-primary)'}}
              />
              <span className="text-lg">{platform.label}</span>
            </label>
          ))}
        </div>
        {errors.platforms && (
          <p className="mt-2 text-lg font-semibold text-red-400">{String(errors.platforms.message)}</p>
        )}
      </div>

      <div className="flex gap-4">
        <button
          type="button"
          className="px-6 py-3 btn-secondary flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          Lưu nháp
        </button>
        <button
          type="button"
          onClick={handleCreateJD}
          disabled={isSubmitting}
          className="px-6 py-3 btn-primary flex items-center gap-2"
          style={{minWidth: '150px', backgroundColor: 'var(--button-primary)', color: 'white'}}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-5 h-5 loading-spinner" />
              <span>Đang tạo JD bằng AI...</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Tạo JD</span>
            </>
          )}
        </button>
      </div>
    </form>

    {showPreview && editableJD && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6" style={{backgroundColor: 'var(--card-bg)', color: 'var(--foreground)'}}>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Job Description - Chỉnh sửa & Xem trước</h2>
            <button
              onClick={() => {
                setShowPreview(false);
                setEditableJD(null);
              }}
              className="px-3 py-1 rounded-md transition-colors duration-200"
              style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', border: '1px solid'}}
            >
              ✕
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-lg font-bold mb-2">Vị trí tuyển dụng</label>
              <input
                type="text"
                value={editableJD.jobTitle || ''}
                onChange={(e) => setEditableJD({...editableJD, jobTitle: e.target.value})}
                className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
                style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-lg font-bold mb-2">Phòng ban</label>
                <input
                  type="text"
                  value={editableJD.department || ''}
                  onChange={(e) => setEditableJD({...editableJD, department: e.target.value})}
                  className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
                  style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                />
              </div>
              <div>
                <label className="block text-lg font-bold mb-2">Địa điểm</label>
                <input
                  type="text"
                  value={editableJD.location || ''}
                  onChange={(e) => setEditableJD({...editableJD, location: e.target.value})}
                  className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
                  style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                />
              </div>
            </div>
            
            <div>
              <label className="block text-lg font-bold mb-2">Mô tả công việc</label>
              <textarea
                value={editableJD.description || ''}
                onChange={(e) => setEditableJD({...editableJD, description: e.target.value})}
                rows={6}
                className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" 
                style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
              />
            </div>
            
            <div>
              <label className="block text-lg font-bold mb-2">Yêu cầu</label>
              <div className="space-y-2">
                {editableJD.requirements?.map((req: string, idx: number) => (
                  <div key={idx} className="flex items-center gap-2">
                    <input
                      type="text"
                      value={req}
                      onChange={(e) => {
                        const newRequirements = [...(editableJD.requirements || [])];
                        newRequirements[idx] = e.target.value;
                        setEditableJD({...editableJD, requirements: newRequirements});
                      }}
                      className="flex-1 px-4 py-2 text-lg font-semibold rounded-md transition-colors duration-200" 
                      style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                    />
                    <button
                      onClick={() => {
                        const newRequirements = editableJD.requirements?.filter((_: string, i: number) => i !== idx) || [];
                        setEditableJD({...editableJD, requirements: newRequirements});
                      }}
                      className="px-3 py-2 rounded-md transition-colors duration-200"
                      style={{backgroundColor: 'var(--button-primary)', color: 'white'}}
                    >
                      Xóa
                    </button>
                  </div>
                ))}
                <button
                  onClick={() => {
                    setEditableJD({...editableJD, requirements: [...(editableJD.requirements || []), '']});
                  }}
                  className="px-4 py-2 rounded-md transition-colors duration-200"
                  style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', border: '1px solid'}}
                >
                  + Thêm yêu cầu
                </button>
              </div>
            </div>
            
            <div>
              <label className="block text-lg font-bold mb-2">Nền tảng đăng tuyển</label>
              <div className="space-y-2">
                {platforms.map(platform => (
                  <label key={platform.id} className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={previewPlatforms.includes(platform.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setPreviewPlatforms([...previewPlatforms, platform.id]);
                        } else {
                          setPreviewPlatforms(previewPlatforms.filter(p => p !== platform.id));
                        }
                      }}
                      className="w-4 h-4"
                    />
                    <span className="text-lg">{platform.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
          
          <div className="flex gap-3 mt-6">
            <button
              onClick={() => {
                setShowPreview(false);
                setEditableJD(null);
              }}
              className="px-4 py-2 rounded-md transition-colors duration-200"
              style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', border: '1px solid'}}
            >
              Hủy
            </button>
            <button
              onClick={handleConfirmPost}
              disabled={isSubmitting || previewPlatforms.length === 0}
              className="px-4 py-2 rounded-md transition-colors duration-200 flex-1 flex items-center justify-center gap-2"
              style={{backgroundColor: 'var(--button-primary)', color: 'white', opacity: (isSubmitting || previewPlatforms.length === 0) ? 0.5 : 1}}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-5 h-5 loading-spinner" />
                  <span>Đang đăng lên nền tảng...</span>
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>Xác nhận đăng lên nền tảng ({previewPlatforms.length})</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    )}
  </Fragment>
  );
}
