'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Upload, Send, FileText, User, Mail, Phone, MapPin } from 'lucide-react';

const applicationSchema = z.object({
  fullName: z.string().min(1, 'Vui lòng nhập họ và tên'),
  email: z.string().email('Email không hợp lệ'),
  phone: z.string().min(10, 'Số điện thoại phải có ít nhất 10 số'),
  address: z.string().min(1, 'Vui lòng nhập địa chỉ'),
  position: z.string().min(1, 'Vui lòng chọn vị trí ứng tuyển'),
  experience: z.enum(['0-1', '1-3', '3-5', '5+']),
  coverLetter: z.string().min(20, 'Thư giới thiệu phải có ít nhất 20 ký tự'),
  cvFile: z.any().refine((file) => file, 'Vui lòng tải lên CV'),
  portfolio: z.string().optional(),
  expectedSalary: z.string().optional(),
  availability: z.string().min(1, 'Vui lòng nhập thời gian có thể bắt đầu'),
});

type ApplicationFormData = z.infer<typeof applicationSchema>;

const positions = [
  'Frontend Developer',
  'Backend Developer',
  'Full Stack Developer',
  'UI/UX Designer',
  'Product Manager',
  'Data Analyst',
  'DevOps Engineer',
  'QA Engineer',
];

const experienceLevels = [
  { value: '0-1', label: 'Dưới 1 năm' },
  { value: '1-3', label: '1-3 năm' },
  { value: '3-5', label: '3-5 năm' },
  { value: '5+', label: 'Trên 5 năm' },
];

export default function ApplyPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [cvFileName, setCvFileName] = useState('');

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<ApplicationFormData>({
    resolver: zodResolver(applicationSchema),
  });

  const cvFile = watch('cvFile');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setValue('cvFile', file);
      setCvFileName(file.name);
    }
  };

  const onSubmit = async (data: ApplicationFormData) => {
    setIsSubmitting(true);
    try {
      console.log('Submitting application:', data);
      
      // Create FormData for file upload
      const formData = new FormData();
      
      // Add all form fields
      formData.append('fullName', data.fullName);
      formData.append('email', data.email);
      formData.append('phone', data.phone);
      formData.append('address', data.address);
      formData.append('position', data.position);
      formData.append('experience', data.experience);
      formData.append('coverLetter', data.coverLetter);
      formData.append('availability', data.availability);
      
      if (data.portfolio) {
        formData.append('portfolio', data.portfolio);
      }
      
      if (data.expectedSalary) {
        formData.append('expectedSalary', data.expectedSalary);
      }
      
      if (data.cvFile) {
        formData.append('cvFile', data.cvFile);
      }

      const submitData = Object.fromEntries(formData);
      const response = await fetch('http://localhost:8000/api/apply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData),
      });

      if (!response.ok) {
        throw new Error('Failed to submit application');
      }

      const result = await response.json();
      console.log('Application submitted successfully:', result);
      
      alert('Hồ sơ đã được nộp thành công! Chúng tôi sẽ liên hệ với bạn sớm.');
      
      // Reset form after successful submission
      // reset();
      
    } catch (error) {
      console.error('Error submitting application:', error);
      alert('Có lỗi xảy ra, vui lòng thử lại.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-full" style={{backgroundColor: 'var(--background)', color: 'var(--foreground)'}}>
      <div className="container mx-auto">
        <div className="card" style={{backgroundColor: 'var(--card-bg)', borderColor: 'var(--card-border)'}}>
          <div className="card-header p-responsive" style={{borderColor: 'var(--card-border)'}}>
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">Ứng Tuyển</h1>
            <p className="mt-4 text-lg md:text-xl lg:text-2xl font-semibold">
              Nộp hồ sơ ứng tuyển cho vị trí bạn quan tâm
            </p>
          </div>
          <div className="p-responsive">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <label className="block text-lg font-bold mb-3">
                    <User className="inline w-4 h-4 mr-1" />
                    Họ và tên *
                  </label>
                  <input
                    {...register('fullName')}
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                    placeholder="Nguyễn Văn A"
                  />
                  {errors.fullName && (
                    <p className="mt-2 text-lg font-semibold text-red-400">{String(errors.fullName.message)}</p>
                  )}
                </div>

                <div>
                  <label className="block text-lg font-bold mb-3">
                    <Mail className="inline w-4 h-4 mr-1" />
                    Email *
                  </label>
                  <input
                    {...register('email')}
                    type="email"
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                    placeholder="email@example.com"
                  />
                  {errors.email && (
                    <p className="mt-2 text-lg font-semibold text-red-400">{String(errors.email.message)}</p>
                  )}
                </div>

                <div>
                  <label className="block text-lg font-bold mb-3">
                    <Phone className="inline w-4 h-4 mr-1" />
                    Số điện thoại *
                  </label>
                  <input
                    {...register('phone')}
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                    placeholder="09xxxxxxxx"
                  />
                  {errors.phone && (
                    <p className="mt-1 text-sm text-red-600">{errors.phone.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-lg font-bold mb-3">
                    <MapPin className="inline w-4 h-4 mr-1" />
                    Địa chỉ *
                  </label>
                  <input
                    {...register('address')}
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                    placeholder="Hà Nội, Việt Nam"
                  />
                  {errors.address && (
                    <p className="mt-1 text-sm text-red-600">{errors.address.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-lg font-bold mb-3">
                    Vị trí ứng tuyển *
                  </label>
                  <select
                    {...register('position')}
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                  >
                    <option value="">Chọn vị trí</option>
                    {positions.map(pos => (
                      <option key={pos} value={pos}>{pos}</option>
                    ))}
                  </select>
                  {errors.position && (
                    <p className="mt-1 text-sm text-red-600">{errors.position.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-lg font-bold mb-3">
                    Kinh nghiệm *
                  </label>
                  <select
                    {...register('experience')}
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                  >
                    <option value="">Chọn kinh nghiệm</option>
                    {experienceLevels.map(level => (
                      <option key={level.value} value={level.value}>
                        {level.label}
                      </option>
                    ))}
                  </select>
                  {errors.experience && (
                    <p className="mt-1 text-sm text-red-600">{errors.experience.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-lg font-bold mb-3">
                    Mức lương mong muốn
                  </label>
                  <input
                    {...register('expectedSalary')}
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                    placeholder="Ví dụ: 15-20 triệu VNĐ"
                  />
                </div>

                <div>
                  <label className="block text-lg font-bold mb-3">
                    Thời gian có thể bắt đầu *
                  </label>
                  <input
                    {...register('availability')}
                    className="w-full px-4 py-3 text-lg font-semibold rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                    placeholder="Ví dụ: Ngay lập tức, 1 tháng nữa"
                  />
                  {errors.availability && (
                    <p className="mt-1 text-sm text-red-600">{errors.availability.message}</p>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-lg font-bold mb-3">
                  Portfolio/LinkedIn (không bắt buộc)
                </label>
                <input
                  {...register('portfolio')}
                  className="w-full px-3 py-2 rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                  placeholder="https://linkedin.com/in/yourprofile"
                />
              </div>

              <div>
                <label className="block text-lg font-bold mb-3">
                  <FileText className="inline w-4 h-4 mr-1" />
                  CV (Resume) *
                </label>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md transition-colors duration-200" style={{borderColor: 'var(--card-border)'}}>
                  <div className="space-y-1 text-center">
                    <Upload className="mx-auto h-16 w-16" style={{color: 'var(--foreground-muted)'}} />
                    <div className="flex text-lg text-secondary">
                      <label
                        htmlFor="cv-upload"
                        className="relative cursor-pointer rounded-md font-medium transition-colors duration-200" style={{color: 'var(--button-primary)'}}
                      >
                        <span>Tải lên file</span>
                        <input
                          id="cv-upload"
                          {...register('cvFile')}
                          type="file"
                          accept=".pdf,.doc,.docx"
                          onChange={handleFileChange}
                          className="sr-only"
                        />
                      </label>
                      <p className="pl-1">hoặc kéo và thả</p>
                    </div>
                    <p className="text-lg text-muted">PDF, DOC, DOCX tối đa 10MB</p>
                    {cvFileName && (
                      <p className="text-lg font-semibold" style={{color: 'var(--button-primary)'}}>
                        Đã chọn: {cvFileName}
                      </p>
                    )}
                  </div>
                </div>
                {errors.cvFile && (
                  <p className="mt-1 text-sm text-red-600">{String(errors.cvFile.message)}</p>
                )}
              </div>

              <div>
                <label className="block text-lg font-bold mb-3">
                  Thư giới thiệu *
                </label>
                <textarea
                  {...register('coverLetter')}
                  rows={6}
                  className="w-full px-3 py-2 rounded-md transition-colors duration-200" style={{backgroundColor: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--foreground)'}}
                  placeholder="Giới thiệu về bản thân, kinh nghiệm, và lý do bạn phù hợp với vị trí này..."
                />
                {errors.coverLetter && (
                  <p className="mt-1 text-sm text-red-600">{String(errors.coverLetter.message)}</p>
                )}
              </div>

              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-6 py-3 btn-primary flex items-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  {isSubmitting ? 'Đang nộp...' : 'Nộp hồ sơ'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
