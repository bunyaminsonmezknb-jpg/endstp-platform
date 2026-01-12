import { createClient } from '@supabase/supabase-js'

// =========================
// SUPABASE CLIENT (FRONTEND)
// =========================

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL!
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY,
  {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
    },
  }
)

// =========================
// BACKEND API BASE
// =========================

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

// =========================
// AUTH – TEK KAYNAK
// =========================

async function getAccessToken(): Promise<string | null> {
  const { data, error } = await supabase.auth.getSession()

  if (error) {
    console.error('Supabase session error:', error.message)
    return null
  }

  return data.session?.access_token ?? null
}

// =========================
// GENERIC API REQUEST
// =========================

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAccessToken()

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`API ${response.status}: ${text}`)
  }

  return response.json() as Promise<T>
}

// =========================
// DOMAIN-SPECIFIC HELPERS
// =========================

export const api = {
  // Subjects
  getSubjects: () =>
    apiRequest<any[]>('/api/v1/subjects'),

  // Topics
  getTopics: (subjectId: string) =>
    apiRequest<any[]>(`/api/v1/topics/${subjectId}`),

  // Student Dashboard
  getStudentDashboard: () =>
    apiRequest<any>('/api/v1/student/dashboard'),

  // Feature flags / health
  getHealthFlags: () =>
    apiRequest<any>('/api/v1/flags/health-status'),
}
