import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'http://localhost:8080/v1',
  apiKey: process.env.OPENAI_API_KEY || 'your-key'
});

async function main() {
  const completion = await client.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'Summarize system metrics.' }]
  });
  console.log(completion.choices[0].message.content);
}

main().catch(console.error);
