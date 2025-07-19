import Head from 'next/head'
import { ArrowRight, Sparkles, Globe, Zap, Target } from 'lucide-react'
import Link from 'next/link'
import { useLanguage } from '../contexts/LanguageContext'

export default function Home() {
  const { t } = useLanguage()

  return (
    <>
      <Head>
        <title>{t('home_title')}</title>
        <meta name="description" content={t('home_description')} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 text-white">
          <div className="container mx-auto px-4 py-20">
            <div className="text-center max-w-4xl mx-auto">
              <h1 className="text-5xl md:text-7xl font-bold mb-6">
                {t('hero_title')}{' '}
                <span className="text-yellow-300 flex items-center justify-center gap-2">
                  {t('ai_power')}
                  <Sparkles className="w-8 h-8 md:w-12 md:h-12" />
                </span>
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-blue-100">
                {t('hero_description')}
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/generator">
                  <button 
                    className="bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold py-4 px-8 rounded-lg text-lg flex items-center justify-center gap-2 transition-all duration-200 transform hover:scale-105"
                  >
                    {t('start_creating')}
                    <ArrowRight className="w-5 h-5" />
                  </button>
                </Link>
                <Link href="/dashboard">
                  <button className="border-2 border-white hover:bg-white hover:text-gray-900 text-white font-bold py-4 px-8 rounded-lg text-lg transition-all duration-200">
                    {t('view_dashboard')}
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
                {t('why_choose_title')}
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                {t('why_choose_subtitle')}
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                  <Sparkles className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{t('feature_ai_title')}</h3>
                <p className="text-gray-600">
                  {t('feature_ai_description')}
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mb-6">
                  <Globe className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{t('feature_regional_title')}</h3>
                <p className="text-gray-600">
                  {t('feature_regional_description')}
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mb-6">
                  <Zap className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{t('feature_platform_title')}</h3>
                <p className="text-gray-600">
                  {t('feature_platform_description')}
                </p>
              </div>

              {/* Feature 4 */}
              <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-orange-100 rounded-lg flex items-center justify-center mb-6">
                  <Target className="w-8 h-8 text-orange-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{t('feature_directions_title')}</h3>
                <p className="text-gray-600">
                  {t('feature_directions_description')}
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-gray-900 text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl font-bold mb-6">
              {t('cta_title')}
            </h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              {t('cta_description')}
            </p>
            <Link href="/generator">
              <button className="bg-yellow-400 hover:bg-yellow-300 text-gray-900 font-bold py-4 px-8 rounded-lg text-lg transition-all duration-200 transform hover:scale-105">
                {t('get_started_now')}
              </button>
            </Link>
          </div>
        </section>
      </main>
    </>
  )
} 