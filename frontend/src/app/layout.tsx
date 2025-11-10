import type { Metadata } from "next";
import { Cairo, Amiri } from "next/font/google";
import { Providers } from "@/components/Providers";
import "./globals.css";

// Arabic display font (headings, UI)
const cairo = Cairo({
  variable: "--font-cairo",
  subsets: ["arabic"],
  display: "swap",
});

// Arabic serif font (poetry, body text)
const amiri = Amiri({
  variable: "--font-amiri",
  weight: ["400", "700"],
  subsets: ["arabic"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "بحر - BAHR Arabic Poetry AI",
  description: "نظام ذكي لتحليل الشعر العربي",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar" dir="rtl">
      <body
        className={`${cairo.variable} ${amiri.variable} antialiased font-sans`}
      >
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
