import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  // ✅ SUPABASE COOKIE'LERİNİ KONTROL ET
  // Supabase kendi cookie'lerini kullanır: sb-<project-ref>-auth-token
  const cookies = req.cookies.getAll()
  const hasSupabaseSession = cookies.some(cookie => 
    cookie.name.startsWith('sb-') && cookie.name.includes('auth-token')
  )

  const protectedRoutes = ['/student', '/test-entry', '/admin', '/reports']
  const isProtectedRoute = protectedRoutes.some(route =>
    req.nextUrl.pathname.startsWith(route)
  )

  const isAuthPage =
    req.nextUrl.pathname === '/login' ||
    req.nextUrl.pathname === '/register'

  console.log('🔍 Middleware:', {
    path: req.nextUrl.pathname,
    hasSession: hasSupabaseSession,
    isProtected: isProtectedRoute,
    isAuth: isAuthPage,
    cookies: cookies.map(c => c.name)
  })

  // 🔒 Protected route + session yok → login
  if (isProtectedRoute && !hasSupabaseSession) {
    console.log('❌ No session, redirect to login')
    return NextResponse.redirect(new URL('/login', req.url))
  }

  // 🔁 Login/Register + session var → dashboard
  if (isAuthPage && hasSupabaseSession) {
    console.log('✅ Has session, redirect to dashboard')
    return NextResponse.redirect(new URL('/student/dashboard', req.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/student/:path*',
    '/test-entry/:path*',
    '/admin/:path*',
    '/reports/:path*',
    '/login',
    '/register',
  ],
}
