'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

interface ExamType {
  id: string;
  code: string;
  name_tr: string;
  short_name: string;
}

interface OsymTopic {
  id: string;
  official_name: string;
  subject_name: string;
  exam_type_id: string;
  related_grade_levels: number[];
  published_year: number;
  exam_types: {
    short_name: string;
  };
}

interface UnmappedTopic {
  id: string;
  name: string;
  subject: string;
  grade: number;
}

export default function OsymManagement() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [examTypes, setExamTypes] = useState<ExamType[]>([]);
  const [osymTopics, setOsymTopics] = useState<OsymTopic[]>([]);
  const [unmappedTopics, setUnmappedTopics] = useState<UnmappedTopic[]>([]);
  
  const [selectedExamType, setSelectedExamType] = useState('');
  const [activeTab, setActiveTab] = useState<'osym' | 'mapping'>('osym');
  
  const [showAddOsym, setShowAddOsym] = useState(false);
  const [newOsym, setNewOsym] = useState({
    exam_type_id: '',
    official_name: '',
    subject_name: '',
    related_grade_levels: [] as number[],
    published_year: 2024
  });
  
  const [showBulkUpload, setShowBulkUpload] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [uploading, setUploading] = useState(false);
  
  const [showAddMapping, setShowAddMapping] = useState(false);
  const [selectedMebTopic, setSelectedMebTopic] = useState('');
  const [selectedOsymTopic, setSelectedOsymTopic] = useState('');
  const [matchType, setMatchType] = useState('exact');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const accessToken = localStorage.getItem('access_token');

        setExamTypes([
          { id: '660e8400-e29b-41d4-a716-446655440001', code: 'TYT', name_tr: 'TYT', short_name: 'TYT' },
          { id: '660e8400-e29b-41d4-a716-446655440002', code: 'AYT', name_tr: 'AYT', short_name: 'AYT' },
        ]);

        const osymRes = await fetch('http://localhost:8000/api/osym/topics', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (osymRes.ok) {
          const data = await osymRes.json();
          setOsymTopics(data.osym_topics);
        }

        const unmappedRes = await fetch('http://localhost:8000/api/admin/unmapped-topics', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (unmappedRes.ok) {
          const data = await unmappedRes.json();
          setUnmappedTopics(data.unmapped_topics);
        }

      } catch (err) {
        console.error('Data fetch hatası:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAddOsym = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
      
      const response = await fetch('http://localhost:8000/api/admin/osym-topics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(newOsym)
      });

      if (response.ok) {
        alert('ÖSYM konusu eklendi!');
        window.location.reload();
      } else {
        alert('Hata oluştu!');
      }
    } catch (err) {
      console.error('Add ÖSYM topic hatası:', err);
    }
  };

  const handleBulkUpload = async () => {
    if (!uploadFile) {
      alert('Lütfen bir dosya seçin!');
      return;
    }

    setUploading(true);
    setUploadResult(null);

    try {
      const accessToken = localStorage.getItem('access_token');
      
      const formData = new FormData();
      formData.append('file', uploadFile);

      const response = await fetch('http://localhost:8000/api/admin/osym-topics/bulk-upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        },
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        setUploadResult(result);
        
        if (result.success) {
          alert(`✅ ${result.success_count} konu başarıyla eklendi!`);
          
          setTimeout(() => {
            window.location.reload();
          }, 2000);
        }
      } else {
        const error = await response.json();
        alert(`Hata: ${error.detail}`);
      }
    } catch (err) {
      console.error('Upload hatası:', err);
      alert('Bir hata oluştu!');
    } finally {
      setUploading(false);
    }
  };

  const handleAddMapping = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
      
      const response = await fetch('http://localhost:8000/api/admin/topic-osym-mapping', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          meb_topic_id: selectedMebTopic,
          osym_topic_id: selectedOsymTopic,
          match_type: matchType,
          match_percentage: matchType === 'exact' ? 100 : 70,
          verified: true,
          created_by: 'admin'
        })
      });

      if (response.ok) {
        alert('Eşleştirme oluşturuldu!');
        window.location.reload();
      } else {
        alert('Hata oluştu!');
      }
    } catch (err) {
      console.error('Add mapping hatası:', err);
    }
  };

  const filteredOsymTopics = selectedExamType
    ? osymTopics.filter(t => t.exam_type_id === selectedExamType)
    : osymTopics;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-800 mx-auto"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <header className="bg-gray-900 text-white shadow-lg border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <div>
              <h1 className="text-2xl font-bold">ÖSYM Konu Yönetimi</h1>
              <p className="text-sm text-gray-400">MEB-ÖSYM Eşleştirme</p>
            </div>
          </div>
          
          <button 
            onClick={() => router.push('/admin')}
            className="px-4 py-2 text-sm bg-gray-700 hover:bg-gray-600 rounded-lg transition"
          >
            Admin Panel
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-md mb-6">
          <div className="border-b border-gray-200">
            <div className="flex gap-2 p-2">
              <button
                onClick={() => setActiveTab('osym')}
                className={`px-6 py-3 rounded-lg font-semibold transition ${
                  activeTab === 'osym'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                ÖSYM Konuları ({osymTopics.length})
              </button>
              <button
                onClick={() => setActiveTab('mapping')}
                className={`px-6 py-3 rounded-lg font-semibold transition ${
                  activeTab === 'mapping'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Eşleştirme ({unmappedTopics.length})
              </button>
            </div>
          </div>
        </div>

        {activeTab === 'osym' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <div className="flex gap-4 items-center">
                <h2 className="text-2xl font-bold text-gray-800">ÖSYM Resmi Konuları</h2>
                
                <select
                  value={selectedExamType}
                  onChange={(e) => setSelectedExamType(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                >
                  <option value="">Tüm Sınavlar</option>
                  {examTypes.map(type => (
                    <option key={type.id} value={type.id}>{type.short_name}</option>
                  ))}
                </select>
              </div>
              
              <div className="flex gap-3">
                <button
                  onClick={() => setShowBulkUpload(true)}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold"
                >
                  Toplu Yükle
                </button>
                
                <button
                  onClick={() => setShowAddOsym(true)}
                  className="px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-semibold"
                >
                  + Tekli Ekle
                </button>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-900 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left">ÖSYM Resmi Adı</th>
                    <th className="px-6 py-4 text-left">Ders</th>
                    <th className="px-6 py-4 text-center">Sınav</th>
                    <th className="px-6 py-4 text-center">Sınıflar</th>
                    <th className="px-6 py-4 text-center">Yıl</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredOsymTopics.length > 0 ? (
                    filteredOsymTopics.map((topic, index) => (
                      <tr key={topic.id} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                        <td className="px-6 py-4 font-semibold text-gray-800">{topic.official_name}</td>
                        <td className="px-6 py-4 text-gray-600">{topic.subject_name}</td>
                        <td className="px-6 py-4 text-center">
                          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-semibold">
                            {topic.exam_types.short_name}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-center text-gray-600">
                          {topic.related_grade_levels.join(', ')}. sınıf
                        </td>
                        <td className="px-6 py-4 text-center text-gray-600">
                          {topic.published_year}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                        <p className="text-lg font-semibold">Henüz ÖSYM konusu eklenmemiş</p>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'mapping' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Konu Eşleştirme</h2>
              
              <button
                onClick={() => setShowAddMapping(true)}
                className="px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-semibold"
                disabled={unmappedTopics.length === 0 || osymTopics.length === 0}
              >
                + Yeni Eşleştirme
              </button>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                Eşleştirilmemiş MEB Konuları
              </h3>
              
              {unmappedTopics.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {unmappedTopics.slice(0, 12).map(topic => (
                    <div key={topic.id} className="p-4 border-2 border-gray-200 rounded-lg hover:border-gray-400 transition">
                      <p className="font-bold text-gray-900">{topic.name}</p>
                      <p className="text-sm text-gray-600">{topic.subject} - {topic.grade}. sınıf</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p className="text-lg font-semibold">Tüm konular eşleştirilmiş!</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {showAddOsym && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Yeni ÖSYM Konusu Ekle</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sınav Türü</label>
                <select
                  value={newOsym.exam_type_id}
                  onChange={(e) => setNewOsym({...newOsym, exam_type_id: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900"
                >
                  <option value="">Seçin</option>
                  {examTypes.map(type => (
                    <option key={type.id} value={type.id}>{type.name_tr}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">ÖSYM Resmi Adı</label>
                <input
                  type="text"
                  value={newOsym.official_name}
                  onChange={(e) => setNewOsym({...newOsym, official_name: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900"
                  placeholder="Örn: Limit ve Süreklilik"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Ders Adı</label>
                <input
                  type="text"
                  value={newOsym.subject_name}
                  onChange={(e) => setNewOsym({...newOsym, subject_name: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900"
                  placeholder="Örn: AYT Matematik"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">İlgili Sınıflar (virgülle)</label>
                <input
                  type="text"
                  placeholder="Örn: 11, 12"
                  onChange={(e) => {
                    const grades = e.target.value.split(',').map(g => parseInt(g.trim())).filter(g => !isNaN(g));
                    setNewOsym({...newOsym, related_grade_levels: grades});
                  }}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900"
                />
              </div>
            </div>

            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowAddOsym(false)}
                className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
              >
                İptal
              </button>
              <button
                onClick={handleAddOsym}
                className="flex-1 px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800"
                disabled={!newOsym.exam_type_id || !newOsym.official_name}
              >
                Ekle
              </button>
            </div>
          </div>
        </div>
      )}

      {showBulkUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Toplu ÖSYM Konusu Yükle</h3>
            
            {!uploadResult ? (
              <>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
                  <input
                    type="file"
                    accept=".xlsx,.xls,.csv"
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    className="hidden"
                    id="excel-upload"
                  />
                  <label htmlFor="excel-upload" className="cursor-pointer">
                    <div className="text-6xl mb-4">📄</div>
                    <p className="text-lg font-semibold text-gray-700 mb-2">
                      {uploadFile ? uploadFile.name : 'Excel dosyası seçin'}
                    </p>
                  </label>
                </div>

                <div className="flex gap-4">
                  <button
                    onClick={() => {
                      setShowBulkUpload(false);
                      setUploadFile(null);
                    }}
                    className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg"
                    disabled={uploading}
                  >
                    İptal
                  </button>
                  <button
                    onClick={handleBulkUpload}
                    className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg"
                    disabled={!uploadFile || uploading}
                  >
                    {uploading ? 'Yükleniyor...' : 'Yükle'}
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
                  <h4 className="font-bold text-lg mb-3 text-green-900">
                    Yükleme Tamamlandı!
                  </h4>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Başarılı:</p>
                      <p className="text-2xl font-bold text-green-600">{uploadResult.success_count}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Hatalı:</p>
                      <p className="text-2xl font-bold text-red-600">{uploadResult.error_count}</p>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setShowBulkUpload(false);
                    setUploadFile(null);
                    setUploadResult(null);
                  }}
                  className="w-full px-6 py-3 bg-gray-900 text-white rounded-lg"
                >
                  Kapat
                </button>
              </>
            )}
          </div>
        </div>
      )}

      {showAddMapping && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Konu Eşleştir</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">MEB Konusu</label>
                <select
                  value={selectedMebTopic}
                  onChange={(e) => setSelectedMebTopic(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900"
                >
                  <option value="">Seçin</option>
                  {unmappedTopics.map(topic => (
                    <option key={topic.id} value={topic.id}>
                      {topic.name} ({topic.subject} - {topic.grade}. sınıf)
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">ÖSYM Konusu</label>
                <select
                  value={selectedOsymTopic}
                  onChange={(e) => setSelectedOsymTopic(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg text-gray-900"
                >
                  <option value="">Seçin</option>
                  {osymTopics.map(topic => (
                    <option key={topic.id} value={topic.id}>
                      {topic.official_name} ({topic.exam_types.short_name})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowAddMapping(false)}
                className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg"
              >
                İptal
              </button>
              <button
                onClick={handleAddMapping}
                className="flex-1 px-6 py-3 bg-gray-900 text-white rounded-lg"
                disabled={!selectedMebTopic || !selectedOsymTopic}
              >
                Eşleştir
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}