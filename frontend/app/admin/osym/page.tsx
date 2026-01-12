'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api/client';

/* ======================================================
   TYPES
====================================================== */

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

/* ======================================================
   API RESPONSE TYPES (⚠️ SADECE TYPE EKLENDİ)
====================================================== */

interface OsymTopicsResponse {
  osym_topics: OsymTopic[];
}

interface UnmappedTopicsResponse {
  unmapped_topics: UnmappedTopic[];
}

interface BulkUploadResponse {
  success: boolean;
  success_count: number;
  error_count: number;
}

/* ======================================================
   COMPONENT
====================================================== */

export default function AdminOsymPage() {
  const router = useRouter();

  const [loading, setLoading] = useState(true);

  const [examTypes, setExamTypes] = useState<ExamType[]>([]);
  const [osymTopics, setOsymTopics] = useState<OsymTopic[]>([]);
  const [unmappedTopics, setUnmappedTopics] = useState<UnmappedTopic[]>([]);

  const [selectedExamType, setSelectedExamType] = useState('');
  const [activeTab, setActiveTab] = useState<'osym' | 'mapping'>('osym');

  const [showAddModal, setShowAddModal] = useState(false);
  const [showBulkUpload, setShowBulkUpload] = useState(false);
  const [showAddMapping, setShowAddMapping] = useState(false);

  const [newOsym, setNewOsym] = useState({
    exam_type_id: '',
    official_name: '',
    subject_name: '',
    related_grade_levels: [] as number[],
    published_year: 2024
  });

  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<BulkUploadResponse | null>(null);
  const [uploading, setUploading] = useState(false);

  const [selectedMebTopic, setSelectedMebTopic] = useState('');
  const [selectedOsymTopic, setSelectedOsymTopic] = useState('');
  const [matchType, setMatchType] = useState<'exact' | 'partial'>('exact');

  /* ======================================================
     DATA FETCH
  ====================================================== */

  useEffect(() => {
    fetchData();
  }, []);

    const fetchData = async () => {
      try {
        setExamTypes([
          { id: '1', code: 'TYT', name_tr: 'TYT', short_name: 'TYT' },
          { id: '2', code: 'AYT', name_tr: 'AYT', short_name: 'AYT' },
        ]);

        const osymRes = await api.get<OsymTopicsResponse>('/api/v1/osym/topics');
        setOsymTopics(osymRes.osym_topics || []);

        const unmappedRes = await api.get<UnmappedTopicsResponse>(
          '/api/v1/admin/unmapped-topics'
        );
        setUnmappedTopics(unmappedRes.unmapped_topics || []);

      } catch (err) {
        console.error('Data fetch hatası:', err);
      } finally {
        setLoading(false);
      }
    };


  /* ======================================================
     ACTIONS
  ====================================================== */

  const handleAddOsym = async () => {
    try {
      await api.post('/api/v1/admin/osym-topics', newOsym);
      alert('✅ ÖSYM konusu eklendi!');
      setShowAddModal(false);
      fetchData();
    } catch (err) {
      console.error('Add ÖSYM topic hatası:', err);
      alert('❌ Hata oluştu!');
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
      const formData = new FormData();
      formData.append('file', uploadFile);

      const res = await api.post<BulkUploadResponse>(
        '/api/v1/admin/osym-topics/bulk-upload',
        formData
      );

      setUploadResult(res);

      if (res.success) {
        setTimeout(() => {
          setShowBulkUpload(false);
          fetchData();
        }, 2000);
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
      await api.post('/api/v1/admin/topic-osym-mapping', {
        meb_topic_id: selectedMebTopic,
        osym_topic_id: selectedOsymTopic,
        match_type: matchType,
        match_percentage: matchType === 'exact' ? 100 : 70,
        verified: true,
        created_by: 'admin'
      });

      alert('✅ Eşleştirme oluşturuldu!');
      setShowAddMapping(false);
      fetchData();
    } catch (err) {
      console.error('Add mapping hatası:', err);
      alert('❌ Hata oluştu!');
    }
  };

  /* ======================================================
     HELPERS
  ====================================================== */

  const filteredTopics = selectedExamType
    ? osymTopics.filter(t => t.exam_type_id === selectedExamType)
    : osymTopics;

  const handleLogout = () => {
    document.cookie = 'access_token=; path=/; max-age=0';
    router.push('/login');
  };

  /* ======================================================
     UI (⚠️ AYNEN KORUNDU)
  ====================================================== */

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">

      {/* HEADER */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">🎯 ÖSYM Konu Yönetimi</h1>
            <p className="text-sm text-gray-500">MEB-ÖSYM Eşleştirme</p>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/admin')}
              className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg"
            >
              ← Admin Panel
            </button>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg"
            >
              Çıkış
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-md mb-6">
          <div className="border-b border-gray-200">
            <div className="flex gap-2 p-2">
              <button onClick={() => setActiveTab('osym')} className={`px-6 py-3 rounded-lg font-semibold ${activeTab === 'osym' ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}>
                📚 ÖSYM Konuları ({osymTopics.length})
              </button>
              <button onClick={() => setActiveTab('mapping')} className={`px-6 py-3 rounded-lg font-semibold ${activeTab === 'mapping' ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}>
                🔗 Eşleştirme ({unmappedTopics.length})
              </button>
            </div>
          </div>
        </div>

        {activeTab === 'osym' && (
          <div>
            <div className="flex justify-between mb-6">
              <div className="flex gap-4">
                <h2 className="text-xl font-bold">ÖSYM Resmi Konuları</h2>
                <select value={selectedExamType} onChange={(e) => setSelectedExamType(e.target.value)} className="px-4 py-2 border-2 border-gray-300 rounded-lg">
                  <option value="">Tüm Sınavlar</option>
                  {examTypes.map(t => <option key={t.id} value={t.id}>{t.short_name}</option>)}
                </select>
              </div>
              <div className="flex gap-3">
                <button onClick={() => setShowBulkUpload(true)} className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold">📤 Toplu</button>
                <button onClick={() => setShowAddModal(true)} className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold">➕ Tekli</button>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-lg overflow-hidden">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left">Resmi Adı</th>
                    <th className="px-6 py-4 text-left">Ders</th>
                    <th className="px-6 py-4 text-center">Sınav</th>
                    <th className="px-6 py-4 text-center">Sınıflar</th>
                    <th className="px-6 py-4 text-center">Yıl</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTopics.length > 0 ? filteredTopics.map((t, i) => (
                    <tr key={t.id} className={`border-b ${i % 2 === 0 ? 'bg-gray-50' : 'bg-white'} hover:bg-blue-50`}>
                      <td className="px-6 py-4 font-semibold">{t.official_name}</td>
                      <td className="px-6 py-4">{t.subject_name}</td>
                      <td className="px-6 py-4 text-center"><span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-semibold">{t.exam_types.short_name}</span></td>
                      <td className="px-6 py-4 text-center">{t.related_grade_levels.join(', ')}. sınıf</td>
                      <td className="px-6 py-4 text-center">{t.published_year}</td>
                    </tr>
                  )) : (
                    <tr><td colSpan={5} className="px-6 py-12 text-center"><div className="text-6xl mb-4">📋</div><p className="text-lg font-semibold">Henüz ÖSYM konusu yok</p></td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'mapping' && (
          <div>
            <div className="flex justify-between mb-6">
              <h2 className="text-xl font-bold">MEB-ÖSYM Eşleştirme</h2>
              <button onClick={() => setShowAddMapping(true)} className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:scale-105 font-semibold shadow-lg" disabled={!unmappedTopics.length || !osymTopics.length}>➕ Yeni Eşleştirme</button>
            </div>
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold mb-4">📝 Eşleştirilmemiş MEB Konuları</h3>
              {unmappedTopics.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {unmappedTopics.slice(0, 12).map(t => (
                    <div key={t.id} className="p-4 border-2 rounded-xl hover:border-purple-500 hover:shadow-lg">
                      <p className="font-bold">{t.name}</p>
                      <p className="text-sm text-gray-600">{t.subject} - {t.grade}. sınıf</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12"><div className="text-6xl mb-4">🎉</div><p className="text-xl font-semibold">Tüm konular eşleştirilmiş!</p></div>
              )}
            </div>
          </div>
        )}
      </main>

      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
            <h3 className="text-2xl font-bold mb-6">➕ Yeni ÖSYM Konusu</h3>
            <div className="space-y-4">
              <select value={newOsym.exam_type_id} onChange={(e) => setNewOsym({...newOsym, exam_type_id: e.target.value})} className="w-full px-4 py-3 border-2 rounded-lg">
                <option value="">Sınav Türü</option>
                {examTypes.map(t => <option key={t.id} value={t.id}>{t.name_tr}</option>)}
              </select>
              <input type="text" value={newOsym.official_name} onChange={(e) => setNewOsym({...newOsym, official_name: e.target.value})} placeholder="ÖSYM Resmi Adı" className="w-full px-4 py-3 border-2 rounded-lg" />
              <input type="text" value={newOsym.subject_name} onChange={(e) => setNewOsym({...newOsym, subject_name: e.target.value})} placeholder="Ders Adı" className="w-full px-4 py-3 border-2 rounded-lg" />
              <input type="text" placeholder="Sınıflar (virgülle)" onChange={(e) => setNewOsym({...newOsym, related_grade_levels: e.target.value.split(',').map(g => parseInt(g.trim())).filter(g => !isNaN(g))})} className="w-full px-4 py-3 border-2 rounded-lg" />
            </div>
            <div className="flex gap-4 mt-6">
              <button onClick={() => setShowAddModal(false)} className="flex-1 px-6 py-3 bg-gray-200 rounded-lg">İptal</button>
              <button onClick={handleAddOsym} className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg" disabled={!newOsym.exam_type_id || !newOsym.official_name}>Ekle</button>
            </div>
          </div>
        </div>
      )}

      {showAddMapping && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
            <h3 className="text-2xl font-bold mb-6">🔗 Konu Eşleştir</h3>
            <div className="space-y-4">
              <select value={selectedMebTopic} onChange={(e) => setSelectedMebTopic(e.target.value)} className="w-full px-4 py-3 border-2 rounded-lg">
                <option value="">MEB Konusu</option>
                {unmappedTopics.map(t => <option key={t.id} value={t.id}>{t.name} ({t.subject} - {t.grade}. sınıf)</option>)}
              </select>
              <select value={selectedOsymTopic} onChange={(e) => setSelectedOsymTopic(e.target.value)} className="w-full px-4 py-3 border-2 rounded-lg">
                <option value="">ÖSYM Konusu</option>
                {osymTopics.map(t => <option key={t.id} value={t.id}>{t.official_name} ({t.exam_types.short_name})</option>)}
              </select>
              <select value={matchType} onChange={(e) => setMatchType(e.target.value as 'exact' | 'partial')} className="w-full px-4 py-3 border-2 rounded-lg">
                <option value="exact">Tam Eşleşme (100%)</option>
                <option value="partial">Kısmi (70%)</option>
              </select>
            </div>
            <div className="flex gap-4 mt-6">
              <button onClick={() => setShowAddMapping(false)} className="flex-1 px-6 py-3 bg-gray-200 rounded-lg">İptal</button>
              <button onClick={handleAddMapping} className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg" disabled={!selectedMebTopic || !selectedOsymTopic}>Eşleştir</button>
            </div>
          </div>
        </div>
      )}

      {showBulkUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
            <h3 className="text-2xl font-bold mb-6">📤 Toplu Yükle</h3>
            {!uploadResult ? (
              <>
                <div className="border-2 border-dashed rounded-xl p-12 text-center mb-6">
                  <input type="file" accept=".xlsx,.xls,.csv" onChange={(e) => setUploadFile(e.target.files?.[0] || null)} className="hidden" id="excel-upload" />
                  <label htmlFor="excel-upload" className="cursor-pointer">
                    <div className="text-6xl mb-4">📄</div>
                    <p className="text-lg font-semibold">{uploadFile ? uploadFile.name : 'Excel seçin'}</p>
                  </label>
                </div>
                <div className="flex gap-4">
                  <button onClick={() => {setShowBulkUpload(false); setUploadFile(null);}} className="flex-1 px-6 py-3 bg-gray-200 rounded-lg">İptal</button>
                  <button onClick={handleBulkUpload} className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg" disabled={!uploadFile || uploading}>{uploading ? 'Yükleniyor...' : 'Yükle'}</button>
                </div>
              </>
            ) : (
              <>
                <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6 mb-6">
                  <h4 className="font-bold text-lg mb-3">✅ Tamamlandı!</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white rounded-lg p-4"><p className="text-sm">Başarılı:</p><p className="text-3xl font-bold text-green-600">{uploadResult.success_count}</p></div>
                    <div className="bg-white rounded-lg p-4"><p className="text-sm">Hatalı:</p><p className="text-3xl font-bold text-red-600">{uploadResult.error_count}</p></div>
                  </div>
                </div>
                <button onClick={() => {setShowBulkUpload(false); setUploadFile(null); setUploadResult(null);}} className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg">Kapat</button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
