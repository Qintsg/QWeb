import { defineStore } from "pinia"

type ModuleCard = {
  code: string
  name: string
  description: string
}

const starterModules: ModuleCard[] = [
  {
    code: "IAM",
    name: "统一身份与权限",
    description: "承接角色、权限覆盖、资源级策略扩展。",
  },
  {
    code: "CONTENT",
    name: "内容平台",
    description: "聚合 Blog、Wiki 与后续媒体能力。",
  },
  {
    code: "TOOLS",
    name: "工具中台",
    description: "为 SSH、FRP、邮件、工作区等高风险模块预留入口。",
  },
]

export const useAppStore = defineStore("app", {
  state: () => ({
    projectName: "QWeb",
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8001",
    modules: starterModules,
  }),
})
