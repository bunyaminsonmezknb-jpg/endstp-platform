import Image from 'next/image';
import WeeklyChart from './WeeklyChart';

export default function Dashboard() {
  const student = {
    name: "Ahmet Yılmaz",
    class: "11. Sınıf",
    totalTests: 24,
    averageNet: 18.5
  };

  const priorityTopics = [
    { id: 1, subject: "Matematik", topic: "Limit", score: 65, priority: "high" },
    { id: 2, subject: "Matematik", topic: "İntegral", score: 40, priority: "urgent" },
    { id: 3, subject: "Fizik", topic: "Manyetizma", score: 80, priority: "medium" },
    { id: 4, subject: "Kimya", topic: "Kimyasal Denge", score: 55, priority: "high" },
  ];

  const getPriorityColor = (priority: string) => {
    switch(priority) {
      case 'urgent': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      default: return 'bg-green-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <span className="text-2xl font-bold text-gray-800">End.STP</span>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-gray-700">👤 {student.name}</span>
            <button className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition">
              Çıkış
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Toplam Test</p>
                <p className="text-3xl font-bold text-blue-600">{student.totalTests}</p>
              </div>
              <div className="text-4xl">📝</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Ortalama Net</p>
                <p className="text-3xl font-bold text-green-600">{student.averageNet}</p>
              </div>
              <div className="text-4xl">📊</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Sınıf</p>
                <p className="text-3xl font-bold text-purple-600">{student.class}</p>
              </div>
              <div className="text-4xl">🎓</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            🎯 Öncelikli Çalışma Konuları
          </h2>
          
          <div className="space-y-4">
            {priorityTopics.map((item) => (
              <div key={item.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <span className={`w-3 h-3 rounded-full ${getPriorityColor(item.priority)}`}></span>
                    <span className="font-semibold text-gray-800">
                      #{item.id} {item.topic}
                    </span>
                    <span className="text-sm text-gray-500">({item.subject})</span>
                  </div>
                  <span className="text-lg font-bold text-gray-700">{item.score}%</span>
                </div>
                
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${item.score}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-8">
          <WeeklyChart />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button className="bg-blue-600 text-white py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition shadow-lg">
            + Yeni Test Ekle
          </button>
          
          <button className="bg-purple-600 text-white py-4 rounded-xl font-semibold text-lg hover:bg-purple-700 transition shadow-lg">
            📈 Raporları Görüntüle
          </button>
        </div>
      </main>
    </div>
  );
}