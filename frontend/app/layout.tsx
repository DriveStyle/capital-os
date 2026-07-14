import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Capital OS',
  description: 'AI-powered Personal Wealth Operating System',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
