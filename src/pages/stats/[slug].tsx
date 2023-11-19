"use client"
import { useRouter } from 'next/router'
 
export default function Page() {
  const router = useRouter();
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="bg-black p-8 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold mb-4">Under Construction</h1>
        <p className="text-gray-600">We are currently working on this page. Please check back later.</p>
        <p className="text-gray-600">Thank you for your patience</p>
        <p className="text-gray-600">Slug: {router.query.slug}</p>
      </div>
    </div>
  );
}