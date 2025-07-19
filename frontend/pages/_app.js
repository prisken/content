import '../styles/globals.css'
import { Toaster } from 'react-hot-toast'
import Layout from '../components/Layout'
import { AuthProvider } from '../contexts/AuthContext'

export default function App({ Component, pageProps }) {
  return (
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
  )
} 