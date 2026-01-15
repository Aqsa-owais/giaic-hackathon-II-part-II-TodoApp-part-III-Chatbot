import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL;

    if (!backendUrl) {
      return res.status(500).json({ error: 'BACKEND_URL not configured' });
    }

    // Test the health endpoint
    const response = await fetch(`${backendUrl}/health`);
    const data = await response.json();

    res.status(response.status).json(data);
  } catch (error) {
    res.status(500).json({ error: 'Could not reach backend', details: (error as Error).message });
  }
}