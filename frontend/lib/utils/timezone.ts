/**
 * Timezone Utility
 * Kullanıcının timezone'unu tespit eder ve saklar
 */

export const getUserTimezone = (): string => {
  try {
    // Tarayıcıdan timezone al
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    
    // localStorage'a kaydet
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_timezone', timezone);
    }
    
    return timezone;
  } catch (error) {
    console.error('Timezone detection error:', error);
    return 'UTC'; // Fallback
  }
};
