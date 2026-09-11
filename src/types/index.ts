export interface CVData {
  name: string
  title: string
  email: string
  phone: string
  location: string
  linkedin: string
  about: string
  age: number
}

export interface Skill {
  name: string
  level: number
  category: string
}

export interface Experience {
  position: string
  company: string
  duration: string
  description: string
  technologies: string[]
}

export interface Education {
  degree: string
  institution: string
  year: string
}

export interface Certificate {
  name: string
  issuer: string
  year: string
}
