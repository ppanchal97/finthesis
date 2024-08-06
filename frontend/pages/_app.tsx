import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import Head from 'next/head';  // Import the Head component

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Finthesis - Personalized News Streaming</title>
      </Head>
      <Component {...pageProps} />
    </>
  );
}
