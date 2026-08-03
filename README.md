# resume-optimizer

                     Browser
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
   Upload JD      Edit Resume      Download PDF
                        │
                        ▼
                FastAPI Backend
                        │
        ┌───────────────┼──────────────────────────┐
        │               │                          │
        ▼               ▼                          ▼
 Resume Service    ATS Service              PDF Service
        │               │                          │
        ▼               ▼                          ▼
Original Resume    AI Optimization          Latex Compiler
        │               │                          │
        └───────────────┼──────────────────────────┘
                        ▼
                  Generated Resume


## Future Architecture

                        Browser
                           │
                   Authentication
                           │
                           ▼
                     FastAPI API
                           │
     ┌──────────────┬───────────────┬──────────────┐
     │              │               │              │
     ▼              ▼               ▼              ▼
 Users         Resume API      Job API      Analysis API
     │              │               │              │
     └──────────────┼───────────────┼──────────────┘
                    ▼
             Service Layer
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Resume Service ATS Service AI Service
      │             │             │
      └─────────────┼─────────────┘
                    ▼
           Repository Layer
                    │
       PostgreSQL / File Storage