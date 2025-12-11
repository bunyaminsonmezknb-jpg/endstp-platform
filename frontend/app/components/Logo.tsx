export default function Logo({ size = 40 }: { size?: number }) {
  return (
    <div className="flex items-center gap-3">
      {/* Placeholder - Sinir ağı ikonu SVG */}
      <div 
        className="relative flex items-center justify-center"
        style={{ width: size, height: size }}
      >
        <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          {/* Nöron dalları */}
          <circle cx="50" cy="30" r="8" fill="#1E40AF" />
          <circle cx="30" cy="55" r="8" fill="#3B82F6" />
          <circle cx="70" cy="55" r="8" fill="#3B82F6" />
          <circle cx="40" cy="80" r="8" fill="#60A5FA" />
          <circle cx="60" cy="80" r="8" fill="#60A5FA" />
          
          {/* Bağlantılar */}
          <line x1="50" y1="30" x2="30" y2="55" stroke="#3B82F6" strokeWidth="3" />
          <line x1="50" y1="30" x2="70" y2="55" stroke="#3B82F6" strokeWidth="3" />
          <line x1="30" y1="55" x2="40" y2="80" stroke="#60A5FA" strokeWidth="3" />
          <line x1="70" y1="55" x2="60" y2="80" stroke="#60A5FA" strokeWidth="3" />
          
          {/* Merkez nöron */}
          <circle cx="50" cy="50" r="12" fill="#1E3A8A" />
        </svg>
      </div>
      
      {/* Text */}
      <div className="flex flex-col">
        <span className="text-xl font-bold text-gray-900">
          End<span className="text-blue-600">.STP</span>
        </span>
        <span className="text-[10px] text-gray-500 -mt-1">Smart Learning Insights</span>
      </div>
    </div>
  );
}