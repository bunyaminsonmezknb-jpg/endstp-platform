'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

type SideDrawerProps = {
  open: boolean;
  title?: string;
  subtitle?: string;
  onClose: () => void;
  children: React.ReactNode;
};

export default function SideDrawer({
  open,
  title,
  subtitle,
  onClose,
  children
}: SideDrawerProps) {
  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50">
          {/* BACKDROP */}
          <motion.div
            className="absolute inset-0 bg-black/40"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          />

          {/* DRAWER PANEL */}
          <motion.div
            className="absolute right-0 top-0 h-full w-full sm:w-[420px] bg-white shadow-2xl"
            initial={{ x: 32, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 32, opacity: 0 }}
            transition={{
              duration: 0.26,
              ease: [0.22, 1, 0.36, 1] // premium easing
            }}
          >
            {/* HEADER */}
            <div className="p-4 border-b">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  {title && (
                    <div className="text-lg font-bold text-gray-900 truncate">
                      {title}
                    </div>
                  )}
                  {subtitle && (
                    <div className="text-sm text-gray-600 mt-0.5">
                      {subtitle}
                    </div>
                  )}
                </div>

                <button
                  onClick={onClose}
                  className="shrink-0 w-9 h-9 rounded-full bg-gray-100 hover:bg-gray-200 transition"
                  aria-label="Kapat"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* CONTENT (STAGGER CONTAINER) */}
            <motion.div
              className="p-4 overflow-y-auto h-[calc(100%-64px)]"
              initial="hidden"
              animate="visible"
              variants={{
                hidden: {},
                visible: {
                  transition: {
                    staggerChildren: 0.035
                  }
                }
              }}
            >
              {React.Children.map(children, (child, i) => (
                <motion.div
                  key={i}
                  variants={{
                    hidden: { opacity: 0, y: 6 },
                    visible: { opacity: 1, y: 0 }
                  }}
                  transition={{ duration: 0.2, ease: 'easeOut' }}
                >
                  {child}
                </motion.div>
              ))}
            </motion.div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
