export default function Home() {
  return (
    <main className="min-h-screen bg-[#0B1F3A] text-white px-6 py-20">

      {/* HERO */}
      <section className="max-w-3xl mx-auto">
        <h1 className="text-5xl font-semibold tracking-tight">
          utsav1033
        </h1>

        <p className="mt-4 text-lg text-blue-200">
          building ML systems + backend infra  
          focused on LLMs, RAG, and scalable APIs
        </p>

        <div className="mt-6 flex gap-6 text-sm text-blue-300">
          <a href="https://github.com/utsav1033" className="hover:underline">
            github
          </a>
          <a href="https://health-kiosk-oaw3.onrender.com" className="hover:underline">
            live app
          </a>
        </div>
      </section>

      {/* WORK */}
      <section className="max-w-3xl mx-auto mt-20">
        <h2 className="text-sm uppercase tracking-widest text-blue-300 mb-6">
          selected work
        </h2>

        <div className="space-y-10">

          <Project
            title="RAG Healthcare Bot"
            desc="retrieval-augmented medical QA system with LLM inference pipeline"
            stack="FastAPI · vector DB · embeddings"
            repo="https://github.com/utsav1033/RAG-Healthcare-Chatbot"
            live="https://health-kiosk-oaw3.onrender.com"
          />

          <Project
            title="Salt Yield Prediction"
            desc="ML pipeline for predicting salt yield for Gujarat pan farmers"
            stack="XGBoost · sklearn · feature engineering"
            repo="https://github.com/utsav1033/Salt-Yield-Prediction"
          />

          <Project
            title="Serverless URL Shortener"
            desc="distributed URL shortener with analytics"
            stack="AWS Lambda · API Gateway · DynamoDB"
            repo="https://github.com/utsav1033/AWS-Serverless-URL-Shortener"
          />

        </div>
      </section>

      {/* SYSTEMS */}
      <section className="max-w-3xl mx-auto mt-20">
        <h2 className="text-sm uppercase tracking-widest text-blue-300 mb-4">
          systems
        </h2>

        <p className="text-blue-100 leading-relaxed">
          building end-to-end ML systems: data pipelines, training workflows,
          retrieval systems, and API deployment. exploring RAG architectures,
          model optimization, and scalable backend design.
        </p>
      </section>

      {/* NOW */}
      <section className="max-w-3xl mx-auto mt-20">
        <h2 className="text-sm uppercase tracking-widest text-blue-300 mb-4">
          now
        </h2>

        <p className="text-blue-100">
          learning C++ DSA (Striver A2Z) · working on text-to-SQL LLM · improving RAG pipelines
        </p>
      </section>

    </main>
  );
}

function Project({ title, desc, stack, repo, live }: any) {
  return (
    <div>
      <h3 className="text-xl font-medium">{title}</h3>

      <p className="text-blue-200 mt-2">{desc}</p>

      <p className="text-xs text-blue-400 mt-2">{stack}</p>

      <div className="mt-2 flex gap-4 text-sm text-blue-300">
        <a href={repo} className="hover:underline">repo</a>
        {live && <a href={live} className="hover:underline">live</a>}
      </div>
    </div>
  );
}