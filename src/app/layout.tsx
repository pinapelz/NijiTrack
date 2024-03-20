import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Footer from '../components/Footer/Footer'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'PhaseTracker - Phase Connect Subscriber Tracker',
  description: 'PhaseTracker, historical subscriber data for members of Phase Connect',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}
      <Footer />
      </body>
      <script defer src="https://analytics.moekyun.me/script.js" data-website-id="c9115390-947a-4077-b885-b136bb813e1a"></script>
    </html>
  )
}
