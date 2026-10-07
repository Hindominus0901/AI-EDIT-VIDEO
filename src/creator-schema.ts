import {z} from 'zod';
export const directorSchema=z.object({
  profile:z.enum(['iman','hormozi','martell']),
  story:z.object({audience:z.string().min(1),premise:z.string().min(1),payoff:z.string().min(1)}),
  framing:z.object({fit:z.enum(['contain','cover']).default('contain'),focusX:z.number().min(0).max(100).default(50),focusY:z.number().min(0).max(100).default(50)}).prefault({}),
  scenes:z.array(z.object({
    id:z.string().min(1),startMs:z.number().nonnegative(),endMs:z.number().positive(),
    layout:z.enum(['speaker','statement','compare','steps','evidence','content-flood','salt-ocean']),
    meaning:z.string().min(1),reason:z.string().min(1),title:z.string().max(85).optional(),
    motion:z.enum(['lift','fade','cut']).default('lift'),
    items:z.array(z.object({text:z.string().max(60),atMs:z.number().nonnegative()})).optional(),
    image:z.string().optional(),assetSource:z.string().optional(),
    callbackTo:z.string().optional(),callbackReason:z.string().optional(),
  })).min(1),
  audioCues:z.array(z.object({startMs:z.number(),endMs:z.number(),gain:z.number().min(0).max(1),reason:z.string()})).default([]),
});
export type Director=z.infer<typeof directorSchema>;
