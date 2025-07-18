# Content Creator Pro - Frontend

This is the frontend application for Content Creator Pro, designed to be deployed on Vercel.

## Features

- **Modern UI/UX**: Built with Next.js and Tailwind CSS
- **Responsive Design**: Mobile-first approach
- **Multi-language Support**: English and Chinese
- **Content Generation**: Step-by-step content creation wizard
- **Image Generation**: AI-powered image generation with style selection
- **Content Library**: Manage and organize generated content
- **Post Management**: Schedule and manage social media posts
- **User Authentication**: Secure login and registration
- **Real-time Updates**: Live content generation and updates

## Tech Stack

- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **HTTP Client**: Axios
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast
- **Icons**: Lucide React
- **Deployment**: Vercel

## Setup Instructions

### 1. Vercel Deployment

1. **Create Vercel Account**: Sign up at [vercel.com](https://vercel.com)

2. **Deploy from GitHub**:
   - Connect your GitHub repository
   - Select the `frontend` folder as the source
   - Vercel will automatically detect the Next.js app

3. **Configure Environment Variables**:
   - Go to your project's "Settings" → "Environment Variables"
   - Add the following variable:
     ```
     BACKEND_URL=https://your-railway-backend-url.railway.app
     ```

4. **Deploy**:
   - Vercel will automatically build and deploy your app
   - You'll get a URL like `https://your-app.vercel.app`

### 2. Local Development

1. **Clone the repository**:
   ```bash
   git clone <your-repo>
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env.local file
   echo "BACKEND_URL=http://localhost:5000" > .env.local
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser**:
   - Navigate to `http://localhost:3000`

## Project Structure

```
frontend/
├── components/          # Reusable React components
├── pages/              # Next.js pages
├── styles/             # Global styles
├── utils/              # Utility functions
├── hooks/              # Custom React hooks
├── types/              # TypeScript type definitions
├── public/             # Static assets
└── package.json        # Dependencies and scripts
```

## Key Components

### Pages
- **Dashboard** (`pages/dashboard.tsx`): Main dashboard with stats and recent content
- **Generator** (`pages/generator.tsx`): Content generation wizard
- **Library** (`pages/library.tsx`): Content management and organization
- **Settings** (`pages/settings.tsx`): User settings and preferences
- **Post Management** (`pages/post-management.tsx`): Social media post management

### Components
- **Header** (`components/Header.tsx`): Navigation and user info
- **ContentCard** (`components/ContentCard.tsx`): Content display card
- **GeneratorSteps** (`components/GeneratorSteps.tsx`): Step-by-step wizard
- **LanguageSelector** (`components/LanguageSelector.tsx`): Language switching
- **ImageGenerator** (`components/ImageGenerator.tsx`): AI image generation

## API Integration

The frontend communicates with the Railway backend through:

1. **Direct API calls**: Using Axios to call backend endpoints
2. **Next.js API routes**: Proxy routes for backend communication
3. **Environment variables**: Backend URL configuration

### Example API Call

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.BACKEND_URL || 'http://localhost:5000',
  withCredentials: true,
});

// Generate content
const generateContent = async (data) => {
  try {
    const response = await api.post('/api/generate', data);
    return response.data;
  } catch (error) {
    console.error('Error generating content:', error);
    throw error;
  }
};
```

## Styling

The app uses Tailwind CSS for styling with:

- **Custom color palette**: Primary and secondary colors
- **Responsive design**: Mobile-first approach
- **Animations**: Fade-in and slide-up animations
- **Dark mode support**: Ready for dark mode implementation

## Internationalization

The app supports multiple languages:

- **English**: Default language
- **Chinese**: Full translation support
- **Language switching**: Real-time language switching
- **Translation keys**: Centralized translation management

## Performance Optimization

- **Next.js optimizations**: Automatic code splitting and optimization
- **Image optimization**: Next.js Image component with Cloudinary
- **Lazy loading**: Components and images loaded on demand
- **Caching**: API responses and static assets cached

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BACKEND_URL` | Railway backend URL | Yes |
| `NEXT_PUBLIC_APP_NAME` | Application name | No |
| `NEXT_PUBLIC_VERSION` | Application version | No |

## Deployment

### Vercel Deployment

1. **Automatic deployment**: Connected to GitHub repository
2. **Preview deployments**: Automatic preview for pull requests
3. **Custom domains**: Add custom domain in Vercel dashboard
4. **Environment variables**: Configure in Vercel dashboard

### Build Process

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Start production server
npm start
```

## Troubleshooting

### Common Issues

1. **Build Errors**:
   - Check Node.js version (requires 18+)
   - Verify all dependencies are installed
   - Check for TypeScript errors

2. **API Connection Issues**:
   - Verify `BACKEND_URL` environment variable
   - Check CORS configuration on backend
   - Ensure backend is running and accessible

3. **Styling Issues**:
   - Clear browser cache
   - Check Tailwind CSS configuration
   - Verify PostCSS configuration

### Development Tips

1. **Hot Reload**: Next.js provides fast refresh for development
2. **TypeScript**: Full TypeScript support for better development experience
3. **ESLint**: Code linting and formatting
4. **Debugging**: Use browser dev tools and Next.js debugging

## Support

For issues and questions:
1. Check Vercel deployment logs
2. Verify environment variables
3. Test API connectivity
4. Review browser console for errors
5. Contact support with specific error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details 