'use client';
import React from 'react';
import { api } from '@/lib/api/client';
import { useTodaysTasks } from '@/lib/api/useTodaysTasks';
import { TopicAtRisk, PriorityTopic } from '@/lib/types/todaysTasks';

// Task interfaces
interface Task {
  id: string;
  task_type: string;
  topic_name: string;
  source_motor: string;
  priority_level: number;
  estimated_time_minutes: number;
  question_count: number | null;
  status: string;
  completed_at: string | null;
  manual_completion?: boolean;
}

interface TasksResponse {
  success: boolean;
  tasks: Task[];
  summary: {
    total_tasks: number;
    completed_tasks: number;
    total_time_minutes: number;
    completed_time_minutes: number;
    remaining_time_minutes: number;
  };
}

// Icons
const AlertIcon = () => <span className="text-2xl">⚠️</span>;
const TargetIcon = () => <span className="text-2xl">🎯</span>;
const FireIcon = () => <span className="text-2xl">🔥</span>;
const ClockIcon = () => <span className="text-xl">⏱️</span>;
const ChartIcon = () => <span className="text-xl">📊</span>;

/**
 * TodayStatusCards Component
 * 
 * Displays 3 key cards + Task list:
 * 1. Unutulmaya Yakın Konular (At Risk Topics)
 * 2. Bugün Çalışılacak Konular (Priority Topics)
 * 3. Zaman Durumu (Streak + Time Stats)
 * 4. Bugünkü Görevlerim (Task list with completion)
 */
export default function TodayStatusCards() {
  const { data, isLoading, error, refetch } = useTodaysTasks();
  
  // Task list states
  const [tasksList, setTasksList] = React.useState<Task[]>([]);
  const [tasksLoading, setTasksLoading] = React.useState(false);
  const [atRiskTopics, setAtRiskTopics] = React.useState<any[]>([]);
  const [totalAtRisk, setTotalAtRisk] = React.useState(0);
  // Fetch tasks on mount
  React.useEffect(() => {
  const fetchTasks = async () => {
    setTasksLoading(true);
    try {
  const tasksData = await api.get('/student/tasks/today') as any;
      if (tasksData.success) {
        setTasksList(tasksData.tasks);
        setAtRiskTopics(tasksData.at_risk_topics || []);
        setTotalAtRisk(tasksData.total_at_risk || 0);
      }
    } catch (err) {
      console.error('Tasks fetch error:', err);
    } finally {
      setTasksLoading(false);
    }
    };
    fetchTasks();
  }, []);

  // Handle task completion
        const handleCompleteTask = async (taskId: string) => {
          try {
            const result = await api.post(`/student/tasks/${taskId}/complete?manual=true`) as any;
            if (result.success) {
              setTasksList(prev =>
                prev.map(t => (t.id === taskId ? { 
                  ...t, 
                  status: 'completed',
                  manual_completion: true,
                  completed_at: new Date().toISOString()
                } : t))
              );
            }
          } catch (err) {
            console.error(err);
          }
        };
// Handle task uncomplete (geri al)
  const handleUncompleteTask = async (taskId: string) => {
    try {
      const result = await api.post(`/student/tasks/${taskId}/uncomplete`) as any;
      if (result.success) {
        setTasksList(prev =>
          prev.map(t => (t.id === taskId ? { ...t, status: 'pending', completed_at: null, manual_completion: false } : t))
        );
      } else {
        alert(result.error || 'Geri alınamadı');
      }
      } catch (err) {
        console.error(err);
      }
  };
  // Loading state
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-white rounded-xl shadow-md p-6 animate-pulse"
          >
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
        <div className="flex items-start gap-3">
          <span className="text-2xl">❌</span>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-red-800 mb-1">
              Veri Yüklenemedi
            </h3>
            <p className="text-red-600 mb-3">{error}</p>
            <button
              onClick={() => refetch()}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Tekrar Dene
            </button>
          </div>
        </div>
      </div>
    );
  }

  // No data state
  if (!data) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-xl p-6 mb-8 text-center">
        <p className="text-gray-600">Henüz veri yok.</p>
      </div>
    );
  }

  return (
    <>
      {/* 3 Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <AtRiskCard 
  topics={data?.at_risk_topics || []} 
  total={data?.total_at_risk || 0} 
/>
        <PriorityCard topics={data.priority_topics} total={data.total_priority} />
        <StreakCard streak={data.streak} timeStats={data.time_stats} />
      </div>

      {/* Task List */}
      <div className="bg-white rounded-2xl p-6 shadow-lg mb-8">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          ✅ Bugünkü Görevlerim ({tasksList.filter(t => t.status === 'completed').length}/{tasksList.length})
        </h3>
        
        {tasksLoading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-purple-600 mx-auto"></div>
          </div>
        ) : (
          <div className="space-y-3">
            {tasksList.map((task) => (
              <div
                key={task.id}
                className={`flex items-center justify-between p-4 rounded-xl border-2 ${
                  task.status === 'completed'
                    ? 'bg-green-50 border-green-300'
                    : 'bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-center gap-4 flex-1">
                  <div className="text-3xl">
                    {task.task_type === 'test' ? '📝' : '📚'}
                  </div>
                  <div>
                    <div className="font-bold text-gray-800">{task.topic_name}</div>
                    <div className="text-sm text-gray-600">
                      {task.task_type === 'test' ? `${task.question_count} soru` : 'Çalışma'} • {task.estimated_time_minutes} dk
                    </div>
                  </div>
                </div>
                
                {task.status === 'completed' ? (
                  <div className="flex items-center gap-3">
                    <div className="text-green-600 font-bold flex items-center gap-2">
                      <span className="text-2xl">✅</span> Tamamlandı
                    </div>
                    {task.manual_completion && (
                      <button
                        onClick={() => handleUncompleteTask(task.id)}
                        className="w-9 h-9 flex items-center justify-center bg-gray-100 hover:bg-gray-200 rounded-full transition-all duration-200 group"
                        title="Geri Al"
                      >
                        <span className="text-xl group-hover:rotate-180 transition-transform duration-300">↺</span>
                      </button>
                    )}
                  </div>
                  ) : (
                    <>
                      {task.task_type === 'test' ? (
                        <div className="text-purple-600 font-semibold flex items-center gap-2">
                          <span>📝</span> Test girişi ile tamamlanacak
                        </div>
                      ) : (
                        <button
                          onClick={() => handleCompleteTask(task.id)}
                          className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
                        >
                          Tamamladım ✓
                        </button>
                      )}
                    </>
                  )}
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}

// ==========================================
// Card 1: Unutulmaya Yakın Konular
// ==========================================
interface AtRiskCardProps {
  topics: TopicAtRisk[];
  total: number;
}

function AtRiskCard({ topics, total }: AtRiskCardProps) {
  // Determine urgency level
  const urgencyLevel =
    total >= 5 ? 'high' : total >= 3 ? 'medium' : total > 0 ? 'low' : 'none';

  const urgencyColors = {
    high: 'bg-red-50 border-red-300',
    medium: 'bg-orange-50 border-orange-300',
    low: 'bg-yellow-50 border-yellow-300',
    none: 'bg-green-50 border-green-300',
  };

  const urgencyTextColors = {
    high: 'text-red-700',
    medium: 'text-orange-700',
    low: 'text-yellow-700',
    none: 'text-green-700',
  };

  return (
    <div
      className={`rounded-xl border-2 p-6 transition-all hover:shadow-lg ${urgencyColors[urgencyLevel]}`}
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <AlertIcon />
        <div className="flex-1">
          <h3 className={`text-lg font-bold ${urgencyTextColors[urgencyLevel]}`}>
            Unutulmaya Yakın
          </h3>
          <p className="text-sm text-gray-600">
            {total === 0 ? 'Harika! Risk yok' : `${total} konu risk altında`}
          </p>
        </div>
      </div>

      {/* Topic List */}
      {total === 0 ? (
        <div className="text-center py-4">
          <span className="text-4xl mb-2 block">✅</span>
          <p className="text-sm text-gray-600">
            Tüm konular güvende!
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {topics.slice(0, 3).map((topic) => (
            <div
              key={topic.topic_id}
              className="bg-white rounded-lg p-3 border border-gray-200"
            >
              <div className="flex items-start justify-between mb-1">
                <h4 className="text-sm font-semibold text-gray-800 flex-1">
                  {topic.topic_name}
                </h4>
                <span className="text-xs font-bold text-red-600 bg-red-100 px-2 py-1 rounded">
                  {topic.days_until_forgotten}g kaldı
                </span>
              </div>
              <p className="text-xs text-gray-500 mb-2">{topic.subject}</p>
              
              {/* Retention Bar */}
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all ${
                    topic.retention_rate < 40
                      ? 'bg-red-500'
                      : topic.retention_rate < 60
                      ? 'bg-orange-500'
                      : 'bg-yellow-500'
                  }`}
                  style={{ width: `${topic.retention_rate}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Akılda Tutma: %{topic.retention_rate}
              </p>
            </div>
          ))}

          {total > 3 && (
            <button className="w-full text-sm text-gray-600 hover:text-gray-800 font-medium py-2">
              + {total - 3} konu daha →
            </button>
          )}
        </div>
      )}

      {/* Action Button */}
      {total > 0 && (
        <button className="w-full mt-4 bg-red-600 text-white py-2.5 rounded-lg font-semibold hover:bg-red-700 transition-colors">
          Hemen Tekrar Et
        </button>
      )}
    </div>
  );
}

// ==========================================
// Card 2: Bugün Çalışılacak Konular
// ==========================================
interface PriorityCardProps {
  topics: PriorityTopic[];
  total: number;
}

function PriorityCard({ topics, total }: PriorityCardProps) {
  const priorityReasonLabels = {
    difficulty: 'Zor',
    retention: 'Unutulmuş',
    prerequisite: 'Temel',
    never_studied: 'Yeni',
  };

  const priorityReasonColors = {
    difficulty: 'bg-purple-100 text-purple-700',
    retention: 'bg-orange-100 text-orange-700',
    prerequisite: 'bg-blue-100 text-blue-700',
    never_studied: 'bg-green-100 text-green-700',
  };

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border-2 border-indigo-200 p-6 transition-all hover:shadow-lg">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <TargetIcon />
        <div className="flex-1">
          <h3 className="text-lg font-bold text-indigo-700">
            Bugün Çalışılacak
          </h3>
          <p className="text-sm text-gray-600">
            {total === 0 ? 'Yeni görev yok' : `${total} öncelikli konu`}
          </p>
        </div>
      </div>

      {/* Topic List */}
      {total === 0 ? (
        <div className="text-center py-4">
          <span className="text-4xl mb-2 block">🎉</span>
          <p className="text-sm text-gray-600">
            Bugün için planlanmış görev yok!
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {topics.slice(0, 3).map((topic) => (
            <div
              key={topic.topic_id}
              className="bg-white rounded-lg p-3 border border-gray-200"
            >
              <div className="flex items-start justify-between mb-1">
                <h4 className="text-sm font-semibold text-gray-800 flex-1">
                  {topic.topic_name}
                </h4>
                <span
                  className={`text-xs font-bold px-2 py-1 rounded ${
                    priorityReasonColors[topic.priority_reason]
                  }`}
                >
                  {priorityReasonLabels[topic.priority_reason]}
                </span>
              </div>
              <p className="text-xs text-gray-500 mb-2">{topic.subject}</p>

              {/* Priority Score */}
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-indigo-600 h-2 rounded-full transition-all"
                    style={{ width: `${topic.priority_score}%` }}
                  ></div>
                </div>
                <span className="text-xs font-bold text-indigo-700">
                  {topic.priority_score}
                </span>
              </div>

              {/* Study Time Estimate */}
              <div className="flex items-center gap-1 mt-2">
                <ClockIcon />
                <span className="text-xs text-gray-600">
                  ~{topic.estimated_study_time} dk
                </span>
              </div>
            </div>
          ))}

          {total > 3 && (
            <button className="w-full text-sm text-gray-600 hover:text-gray-800 font-medium py-2">
              + {total - 3} konu daha →
            </button>
          )}
        </div>
      )}

      {/* Action Button */}
      {total > 0 && (
        <button className="w-full mt-4 bg-indigo-600 text-white py-2.5 rounded-lg font-semibold hover:bg-indigo-700 transition-colors">
          Çalışmaya Başla
        </button>
      )}
    </div>
  );
}

// ==========================================
// Card 3: Zaman Durumu (Streak + Time)
// ==========================================
interface StreakCardProps {
  streak: {
    current_streak: number;
    longest_streak: number;
    streak_status: 'active' | 'at_risk' | 'broken';
    last_study_date: string;
    next_milestone: number;
  };
  timeStats: {
    total_study_time_today: number;
    total_study_time_week: number;
    avg_daily_time: number;
    target_daily_time: number;
    time_efficiency: number;
  };
}

function StreakCard({ streak, timeStats }: StreakCardProps) {
  const streakStatusColors = {
    active: 'bg-green-50 border-green-300',
    at_risk: 'bg-yellow-50 border-yellow-300',
    broken: 'bg-gray-50 border-gray-300',
  };

  const streakStatusText = {
    active: 'Devamlılık Aktif!',
    at_risk: 'Devamlılık Risk Altında',
    broken: 'Devamlılık Kırıldı',
  };

  const streakStatusTextColor = {
    active: 'text-green-700',
    at_risk: 'text-yellow-700',
    broken: 'text-gray-700',
  };

  // Calculate progress to next milestone
  const milestoneProgress = (streak.current_streak / streak.next_milestone) * 100;

  // Calculate today's time progress
  const todayProgress = (timeStats.total_study_time_today / timeStats.target_daily_time) * 100;

  return (
    <div
      className={`rounded-xl border-2 p-6 transition-all hover:shadow-lg ${streakStatusColors[streak.streak_status]}`}
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <FireIcon />
        <div className="flex-1">
          <h3 className={`text-lg font-bold ${streakStatusTextColor[streak.streak_status]}`}>
            {streakStatusText[streak.streak_status]}
          </h3>
          <p className="text-sm text-gray-600">
            {streak.current_streak} gün üst üste
          </p>
        </div>
      </div>

      {/* Streak Info */}
      <div className="bg-white rounded-lg p-4 mb-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm text-gray-600">Mevcut Devamlılık</span>
          <span className="text-2xl font-bold text-orange-600">
            {streak.current_streak} 🔥
          </span>
        </div>

        <div className="flex items-center justify-between mb-3">
          <span className="text-sm text-gray-600">En Uzun Devamlılık</span>
          <span className="text-lg font-semibold text-gray-700">
            {streak.longest_streak} gün
          </span>
        </div>

        {/* Milestone Progress */}
        <div className="mb-2">
          <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
            <span>Hedef: {streak.next_milestone} gün</span>
            <span>{Math.round(milestoneProgress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-orange-500 h-2 rounded-full transition-all"
              style={{ width: `${Math.min(milestoneProgress, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Time Stats */}
      <div className="bg-white rounded-lg p-4">
        <div className="flex items-center gap-2 mb-3">
          <ChartIcon />
          <span className="text-sm font-semibold text-gray-700">
            Bugünkü Çalışma
          </span>
        </div>

        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600">Süre</span>
          <span className="text-lg font-bold text-indigo-600">
            {timeStats.total_study_time_today} dk
          </span>
        </div>

        {/* Today's Progress Bar */}
        <div className="mb-3">
          <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
            <span>Hedef: {timeStats.target_daily_time} dk</span>
            <span>{Math.round(todayProgress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${
                todayProgress >= 100
                  ? 'bg-green-500'
                  : todayProgress >= 75
                  ? 'bg-blue-500'
                  : todayProgress >= 50
                  ? 'bg-yellow-500'
                  : 'bg-orange-500'
              }`}
              style={{ width: `${Math.min(todayProgress, 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs text-gray-600">
          <span>Bu Hafta Toplam</span>
          <span className="font-semibold">{timeStats.total_study_time_week} dk</span>
        </div>
      </div>

      {/* Action Button */}
      <button className="w-full mt-4 bg-orange-600 text-white py-2.5 rounded-lg font-semibold hover:bg-orange-700 transition-colors">
        Devamlılığını Koru
      </button>
    </div>
  );
}
