/**
 * Example verses component - clickable examples for users to try
 */

"use client";

interface ExampleVerse {
  text: string;
  poet: string;
  meter: string;
}

const examples: ExampleVerse[] = [
  {
    text: "إذا غامرت في شرف مروم *** فلا تقنع بما دون النجوم",
    poet: "المتنبي",
    meter: "الطويل",
  },
  {
    text: "قفا نبك من ذكرى حبيب ومنزل *** بسقط اللوى بين الدخول فحومل",
    poet: "امرؤ القيس",
    meter: "الطويل",
  },
  {
    text: "أَلا لَيتَ الشَبابَ يَعودُ يَوماً *** فَأُخبِرَهُ بِما فَعَلَ المَشيبُ",
    poet: "أبو العتاهية",
    meter: "الوافر",
  },
];

interface ExampleVersesProps {
  onSelect: (text: string) => void;
  disabled?: boolean;
}

export function ExampleVerses({
  onSelect,
  disabled = false,
}: ExampleVersesProps) {
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-gray-700 flex items-center gap-2">
        <svg
          className="w-4 h-4 text-blue-600"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
        </svg>
        أو جرّب أحد الأمثلة:
      </h3>
      <div className="grid gap-2">
        {examples.map((example, index) => (
          <button
            key={index}
            onClick={() => onSelect(example.text)}
            disabled={disabled}
            className="text-right p-4 bg-gradient-to-l from-blue-50 to-white border border-blue-200 rounded-lg hover:border-blue-400 hover:shadow-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-blue-200 disabled:hover:shadow-none group"
          >
            <p
              dir="rtl"
              className="font-[family-name:var(--font-amiri)] text-base text-gray-800 mb-2 leading-relaxed"
            >
              {example.text}
            </p>
            <div className="flex items-center justify-between text-xs">
              <span className="text-gray-600">— {example.poet}</span>
              <span className="text-blue-600 font-medium bg-blue-100 px-2 py-1 rounded group-hover:bg-blue-200 transition-colors">
                {example.meter}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
