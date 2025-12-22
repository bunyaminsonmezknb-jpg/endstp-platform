'use client';

import { getSubjectIcon, isAdvancedSubject, getSubjectGradient } from '@/lib/icons/subjectIcons';
import React from 'react';

interface SubjectIconProps {
  subjectCode: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'card' | 'compact';
  showBadge?: boolean;
  className?: string;
}

export default function SubjectIcon({ 
  subjectCode, 
  size = 'md',
  variant = 'card',
  showBadge = false,
  className = '' 
}: SubjectIconProps) {
  const config = getSubjectIcon(subjectCode);
  const isAdvanced = isAdvancedSubject(subjectCode);

  // COMPACT VARIANT (Dropdown için)
  if (variant === 'compact') {
    const compactSizeClasses = {
      sm: 'w-4 h-4',
      md: 'w-5 h-5',
      lg: 'w-6 h-6',
      xl: 'w-7 h-7'
    };

    return (
      <div className={`flex-shrink-0 ${className}`}>
        <div className={`${compactSizeClasses[size]} text-gray-600`}>
          {React.cloneElement(config.icon as React.ReactElement, {
            className: compactSizeClasses[size]
          })}
        </div>
      </div>
    );
  }

  // CARD VARIANT (Progress için)
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-20 h-20'
  };

  const iconSizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-10 h-10'
  };

  const badgeSizeClasses = {
    sm: 'w-3 h-3 text-[8px]',
    md: 'w-4 h-4 text-[10px]',
    lg: 'w-5 h-5 text-xs',
    xl: 'w-6 h-6 text-sm'
  };

  return (
    <div className={`relative ${className}`}>
      <div className={`
        ${sizeClasses[size]}
        bg-gradient-to-br ${getSubjectGradient(subjectCode)}
        rounded-lg flex items-center justify-center shadow-md
        transition-all duration-200 hover:shadow-lg hover:scale-105
      `}>
        <div className={`${iconSizeClasses[size]} text-white`}>
          {React.cloneElement(config.icon as React.ReactElement, {
            className: iconSizeClasses[size]
          })}
        </div>
      </div>

      {showBadge && (
        <div className={`
          absolute -bottom-1 -right-1
          ${badgeSizeClasses[size]}
          rounded-full flex items-center justify-center font-bold shadow-sm
          ${isAdvanced 
            ? 'bg-yellow-400 text-yellow-900' 
            : 'bg-white text-gray-600 border-2 border-gray-200'
          }
        `}>
          {isAdvanced ? '⭐' : '○'}
        </div>
      )}
    </div>
  );
}