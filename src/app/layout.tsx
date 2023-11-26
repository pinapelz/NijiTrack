import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Footer from '../components/Footer/Footer'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'PhaseTracker - Phase Connect Subscriber Tracker',
  description: 'Nijitracker, historical subscriber data for members of Phase Connect',
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
    </html>
  )
}
