import Head from 'next/head'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Footer from '../components/Footer/Footer'
import { Analytics } from "@vercel/analytics/react"
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
      <Analytics/>
      </body>
    </html>
  )
}