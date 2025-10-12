<script setup>
import { ref, computed } from 'vue'
import { SplitterGroup, SplitterPanel, SplitterResizeHandle } from 'reka-ui'
import Chatbot from "@/components/dashboard/Chatbot.vue"
import CreateTicket from "@/components/dashboard/CreateTicket.vue"
import ViewTicket from "@/components/dashboard/ViewTicket.vue"
// Active menu state
const activeMenu = ref('View Issues')
const panelCollapsed = ref(false)
const sidebarPanelRef = ref(null)

// Menu items for sidebar
const menuItems = [
  { name: 'View Issues' },
  { name: 'Chatbot' },
  { name: 'Create Issues' }
]

// Current content background based on active menu

// Set active menu
const setActiveMenu = (menuName) => {
  activeMenu.value = menuName
}

// Toggle collapse/expand using the panel's built-in methods
const toggleCollapse = () => {
  if (sidebarPanelRef.value) {
    if (panelCollapsed.value) {
      sidebarPanelRef.value.expand()
    } else {
      sidebarPanelRef.value.collapse()
    }
  }
}

// Handle panel collapse event
const handleCollapse = () => {
  panelCollapsed.value = true
}

// Handle panel expand event
const handleExpand = () => {
  panelCollapsed.value = false
}
</script>

<template>
  <div class="flex h-screen  bg-gray-50">
    <SplitterGroup direction="horizontal" class="h-full w-full">
      <SplitterPanel
        ref="sidebarPanelRef"
        :min-size="12"
        :default-size="15"
        :max-size="30"
        :collapsed-size="0"
        collapsible
        @collapse="handleCollapse"
        @expand="handleExpand"
        class="min-w-0 transition-all duration-300"
      >
        <aside
          class="bg-white h-full flex flex-col"
          :class="panelCollapsed ? 'w-0 overflow-hidden' : 'w-full'"
        >
          <div class="p-6 flex items-center justify-between border-b border-gray-100">
            <h1
              class="text-lg font-medium! text-gray-900 transition-opacity duration-300"
              :class="panelCollapsed ? 'opacity-0' : 'opacity-100'"
            >
              Dashboard
            </h1>
            <button
              @click="toggleCollapse"
              class="p-1.5 text-gray-500 hover:text-gray-700"
              :aria-expanded="panelCollapsed"
              :aria-controls="'sidebar-content'"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                class="transition-transform duration-300"
                :class="{ 'rotate-180!': !panelCollapsed }"
                fill="currentColor"
              >
                <path d="M10.061 19.061 17.121 12l-7.06-7.061-2.122 2.122L12.879 12l-4.94 4.939z"></path>
              </svg>
            </button>
          </div>

          <nav
            id="sidebar-content"
            class="mt-2 flex-1 transition-opacity duration-300 px-3"
            :class="panelCollapsed ? 'opacity-0' : 'opacity-100'"
          >
            <ul class="space-y-1">
              <li v-for="item in menuItems" :key="item.name">
                <button
                  @click="setActiveMenu(item.name)"
                  class="flex items-center w-full px-3 py-4 rounded-lg text-left text-[15px]
                  font-medium! transition-all duration-200"
                  :class="activeMenu === item.name ?
                    'bg-gray-900 text-white' :
                    'text-gray-700 hover:bg-gray-50'"
                >
                  <span>{{ item.name }}</span>
                </button>
              </li>
            </ul>
          </nav>
        </aside>
      </SplitterPanel>

      <SplitterResizeHandle
        class="w-1.5 bg-gray-100 hover:bg-gray-300 transition-colors duration-150 cursor-col-resize relative"
      >
        <button
          v-if="panelCollapsed"
          @click="toggleCollapse"
          class="absolute w-6 h-6 z-100 block top-[28px] scale-125 left-1/2 -translate-x-1/20"
:class="panelCollapsed ? 'rotate-180!' : ''"

          title="Expand sidebar"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M13.939 4.939 6.879 12l7.06 7.061 2.122-2.122L11.121 12l4.94-4.939z"></path>
          </svg>
        </button>
      </SplitterResizeHandle>

      <SplitterPanel class="flex-1 flex flex-col overflow-hidden">
        <header class="bg-white shadow-sm z-10">
          <div class="flex items-center justify-between px-6 py-4">
            <div class="flex-1">
              <h2 class="text-xl font-semibold! text-teal-800"
:class="panelCollapsed ? 'pl-4' : ''"

                >{{ activeMenu }}</h2>
            </div>
            <div class="flex flex-row items-center justify-center gap-4">
              <button class="bg-gray-200/5 px-4 border-2 border-teal-600/20 py-2 rounded-md
                font-medium! hover:bg-teal-50 transition-colors duration-200">
                Help
              </button>
              <button class="text-gray-600 font-medium! hover:text-teal-700 transition-colors duration-200 flex flex-row gap-2 px-4 border-2 border-teal-600/20 py-2 rounded-md hover:bg-teal-50">
                <svg width="24px" height="24px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentColor">
                  <path d="M9 9C9 5.49997 14.5 5.5 14.5 9C14.5 11.5 12 10.9999 12 13.9999" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                  <path d="M12 18.01L12.01 17.9989" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                  <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 13.8214 2.48697 15.5291 3.33782 17L2.5 21.5L7 20.6622C8.47087 21.513 10.1786 22 12 22Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                </svg>
                Report Issues
              </button>
            </div>
          </div>
        </header>

        <main class="flex-1 overflow-auto">
          <div :class="['h-full flex items-center justify-center text-center']"
            v-if="activeMenu === 'Chatbot'">
            <Chatbot/>
          </div>
  <div :class="['h-full flex items-center justify-center text-center']"
            v-if="activeMenu === 'View Issues'">
    <ViewTicket/>
          </div>
  <div :class="['h-full flex items-center justify-center text-center']"
            v-if="activeMenu === 'Create Issues'">
    <CreateTicket/>
          </div>

        </main>
      </SplitterPanel>
    </SplitterGroup>
  </div>
</template>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
