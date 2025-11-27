import { redirect } from 'next/navigation';

export default function Home() {
  // Eğer token varsa dashboard'a, yoksa login'e
  redirect('/student/dashboard');
}
