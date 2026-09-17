/**
 * Core CV data types
 */

export interface Skill {
  name: string;
  level?: 'beginner' | 'intermediate' | 'advanced' | 'expert';
}

export interface SkillCategory {
  category: string;
  skills: Skill[];
}

export interface Experience {
  id: string;
  title: string;
  company: string;
  period: string;
  description: string;
  technologies?: string[];
  achievements?: string[];
}

export interface Education {
  id: string;
  degree: string;
  institution: string;
  graduation: string;
  description?: string;
}

export interface Certificate {
  id: string;
  name: string;
  issuer: string;
  date: string;
  credentialURL?: string;
  hours?: number;
}

export interface Profile {
  name: string;
  title: string;
  email: string;
  phone?: string;
  location: string;
  bio: string;
  github: string;
  linkedin: string;
  portfolio: string;
}

export interface CV_Data {
  profile: Profile;
  skills: SkillCategory[];
  experience: Experience[];
  education: Education[];
  certificates: Record<string, Certificate[]>;
  languages?: string[];
}
