import '../styles/globals.css'
import { Toaster } from 'react-hot-toast'
import Layout from '../components/Layout'
import { AuthProvider } from '../contexts/AuthContext'
import { LanguageProvider } from '../contexts/LanguageContext'

export default function App({ Component, pageProps }) {
  return (
    <LanguageProvider>
      <AuthProvider>
        <Layout>
          <Component {...pageProps} />
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </Layout>
      </AuthProvider>
    </LanguageProvider>
  )
} 