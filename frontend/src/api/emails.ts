// src/api/emails.ts
import { api } from "./client";

export type EmailCategory =
  | "FEEDBACK_NEGATIVO"
  | "FEEDBACK_POSITIVO"
  | "GARANTIA"
  | "ARREPENDIMENTO_REEMBOLSO"
  | "DUVIDAS_GERAIS"
  | "INCONCLUSIVO";

export interface Email {
  id: number;
  from_email: string;
  subject: string;
  body: string;
  category: EmailCategory;
  confidence: number;
  draft_reply: string;
  requires_human_review: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateEmailPayload {
  from_email: string;
  subject: string;
  body: string;
}

export interface UpdateEmailPayload {
  category?: EmailCategory;
  draft_reply?: string;
  requires_human_review?: boolean;
}

export async function classifyEmail(payload: CreateEmailPayload) {
  const { data } = await api.post<Email>("/emails/classify", payload);
  return data;
}

export async function listEmails() {
  const { data } = await api.get<Email[]>("/emails");
  return data;
}

export async function updateEmail(id: number, payload: UpdateEmailPayload) {
  const { data } = await api.put<Email>(`/emails/${id}`, payload);
  return data;
}