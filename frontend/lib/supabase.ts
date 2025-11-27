import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Auth helpers
export const auth = {
  signIn: async (email: string, password: string) => {
    return await supabase.auth.signInWithPassword({
      email,
      password,
    })
  },

  signUp: async (email: string, password: string) => {
    return await supabase.auth.signUp({
      email,
      password,
    })
  },

  signOut: async () => {
    return await supabase.auth.signOut()
  },

  getSession: async () => {
    return await supabase.auth.getSession()
  },

  getUser: async () => {
    return await supabase.auth.getUser()
  },
}
