import Head from 'next/head'
import { useState } from 'react'
import { ArrowRight, Sparkles, Globe, Zap, Target } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)

  return (
    <>
      <Head>
        <title>Content Creator Pro - AI-Powered Content Generation</title>
        <meta name="description" content="Generate professional social media posts, blog articles, and more with our AI-powered platform. Choose from 18 content directions and create content that resonates with your audience." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 text-white">
          <div className="container mx-auto px-4 py-20">
            <div className="text-center max-w-4xl mx-auto">
              <h1 className="text-5xl md:text-7xl font-bold mb-6">
                Create Engaging Content with{' '}
                <span className="text-yellow-300 flex items-center justify-center gap-2">
                  AI Power
                  <Sparkles className="w-8 h-8 md:w-12 md:h-12" />
                </span>
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-blue-100">
                Generate professional social media posts, blog articles, and more with our AI-powered platform. 
                Choose from 18 content directions and create content that resonates with your audience.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/generator">
                  <button 
                    className="bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold py-4 px-8 rounded-lg text-lg flex items-center justify-center gap-2 transition-all duration-200 transform hover:scale-105"
                    onClick={() => setIsLoading(true)}
                  >
                    Start Creating
                    <ArrowRight className="w-5 h-5" />
                  </button>
                </Link>
                <Link href="/dashboard">
                  <button className="border-2 border-white hover:bg-white hover:text-gray-900 text-white font-bold py-4 px-8 rounded-lg text-lg transition-all duration-200">
                    View Dashboard
                  </button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Why Choose Content Creator Pro?
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Everything you need to create engaging content
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                  <Sparkles className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">AI-Powered Generation</h3>
                <p className="text-gray-600">
                  Advanced AI models create high-quality, engaging content tailored to your needs.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                  <Globe className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Regional Adaptation</h3>
                <p className="text-gray-600">
                  Content automatically adapts to your region with cultural sensitivity and local relevance.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                  <Zap className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Multi-Platform Support</h3>
                <p className="text-gray-600">
                  Create content for LinkedIn, Facebook, Instagram, Twitter, YouTube, and blogs.
                </p>
              </div>

              {/* Feature 4 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-orange-100 rounded-lg flex items-center justify-center mb-6">
                  <Target className="w-8 h-8 text-orange-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Content Directions</h3>
                <p className="text-gray-600">
                  Choose from 18 specialized content directions for targeted content creation.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gray-900 text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl font-bold mb-6">
              Ready to Create Amazing Content?
            </h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Join thousands of creators who are already using Content Creator Pro to generate engaging content.
            </p>
            <Link href="/generator">
              <button className="bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold py-4 px-8 rounded-lg text-lg transition-all duration-200 transform hover:scale-105">
                Get Started Now
              </button>
            </Link>
          </div>
        </section>
      </main>
    </>
  )
} 