import JDForm from './components/JDForm';

export default function Home() {
  return (
    <div className="min-h-full" style={{backgroundColor: 'var(--background)', color: 'var(--foreground)'}}>
      <div className="container mx-auto">
        <div className="card fade-in" style={{backgroundColor: 'var(--card-bg)', borderColor: 'var(--card-border)'}}>
          <div className="card-header p-responsive" style={{borderColor: 'var(--card-border)'}}>
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-extrabold">Tạo Job Description</h1>
            <p className="mt-4 text-lg md:text-xl lg:text-2xl font-semibold">
              Tạo mô tả công việc và đăng lên các nền tảng tuyển dụng
            </p>
          </div>
          <div className="card-body">
            <JDForm />
          </div>
        </div>
      </div>
    </div>
  );
}
