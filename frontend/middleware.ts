import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const token = req.cookies.get('access_token')?.value;
  
  // Protected routes
  const protectedRoutes = ['/student', '/test-entry', '/admin', '/reports'];
  const isProtectedRoute = protectedRoutes.some(route => req.nextUrl.pathname.startsWith(route));
  const isLoginPage = req.nextUrl.pathname === '/login';

  // Protected route'a token olmadan girilmeye çalışılıyor
  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  // Token varken login sayfasına girilmeye çalışılıyor
  if (isLoginPage && token) {
    return NextResponse.redirect(new URL('/student/dashboard', req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/student/:path*', 
    '/test-entry/:path*', 
    '/admin/:path*', 
    '/reports/:path*', 
    '/login'
  ],
}
