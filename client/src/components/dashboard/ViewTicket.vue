<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
    <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

      <header class="mb-8">
        <div class="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
          <div>
            <h1 class="text-3xl font-bold tracking-tight text-gray-900">Ticket Management</h1>
            <p class="mt-1 text-sm text-gray-600">Track, manage, and resolve all support tickets
            efficiently.</p>View
          </div>

          <div class="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
            <div class="relative flex-grow">
              <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
              </span>
              <input
                v-model="searchKeyword"
                @keyup.enter="handleSearch"
                type="text"
                placeholder="Search by keyword..."
                class="w-full rounded-lg border-gray-300 py-2 pl-10 pr-4 shadow-sm transition duration-150 ease-in-out focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 sm:min-w-[300px]"
              />
            </div>
            <button
              @click="fetchTickets"
              class="flex items-center justify-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm transition-colors hover:bg-gray-50"
              aria-label="Refresh tickets"
            >
              <ArrowPathIcon class="h-5 w-5" />
              <span>Refresh</span>
            </button>
          </div>
        </div>
      </header>

      <div class="mb-8 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Filters</h3>
          <button
            @click="clearFilters"
            class="-my-2 -mr-2 px-3 py-2 text-sm font-medium text-blue-600 transition hover:bg-blue-50 hover:text-blue-700"
          >
            Clear All
          </button>
        </div>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-4">
          <FilterSelect v-model="filters.status" @update:modelValue="applyFilters" label="Status" default-option="All Statuses">
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="pending">Pending</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </FilterSelect>
          <FilterSelect v-model="filters.priority" @update:modelValue="applyFilters" label="Priority" default-option="All Priorities">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </FilterSelect>
          <FilterSelect v-model="filters.category" @update:modelValue="applyFilters" label="Category" default-option="All Categories">
            <option value="bug">Bug</option>
            <option value="feature">Feature Request</option>
            <option value="support">Support</option>
            <option value="enhancement">Enhancement</option>
          </FilterSelect>
        </div>
      </div>

      <main>
        <div v-if="loading" class="flex flex-col items-center justify-center rounded-xl bg-white p-16 text-center shadow-sm">
          <ArrowPathIcon class="mb-4 h-12 w-12 animate-spin text-blue-600" />
          <p class="text-lg font-semibold text-gray-700">Fetching Tickets...</p>
          <p class="mt-1 text-sm text-gray-500">Please wait a moment.</p>
        </div>

        <div v-else-if="error" class="rounded-xl border border-red-200 bg-red-50 p-6 shadow-sm">
          <div class="flex items-start gap-4">
            <ExclamationTriangleIcon class="h-6 w-6 flex-shrink-0 text-red-500" />
            <div>
              <h3 class="font-semibold text-red-800">Oops, something went wrong.</h3>
              <p class="mt-1 text-sm text-red-700">{{ error }}</p>
              <button @click="fetchTickets" class="mt-4  bg-red-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-red-700">
                Try Again
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="tickets.length > 0" class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
          <div class="overflow-x-auto">
            <table class="w-full table-auto">
              <thead class="border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold uppercase tracking-wider text-gray-600">
                <tr>
                  <th class="px-6 py-4">Ticket #</th>
                  <th class="px-6 py-4">Title</th>
                  <th class="px-6 py-4">Priority</th>
                  <th class="px-6 py-4">Status</th>
                  <th class="px-6 py-4">Assigned To</th>
                  <th class="px-6 py-4">Created</th>
                  <th class="px-6 py-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="ticket in tickets" :key="ticket.id" class="group transition-colors hover:bg-gray-50">
                  <td class="whitespace-nowrap px-6 py-4 font-mono text-sm font-medium text-gray-800">{{ ticket.ticket_number }}</td>
                  <td class="max-w-xs px-6 py-4">
                    <p class="truncate text-sm font-semibold text-gray-900 transition-colors group-hover:text-blue-600">{{ ticket.title }}</p>
                    <p class="truncate text-xs text-gray-500">{{ ticket.category }}</p>
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm">
                    <StatusBadge :class="getPriorityClass(ticket.priority)">
                      {{ formatTitle(ticket.priority) }}
                    </StatusBadge>
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm">
                    <StatusBadge :class="getStatusClass(ticket.status)">
                      {{ formatTitle(ticket.status) }}
                    </StatusBadge>
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm">
                    <div class="flex items-center gap-2">
                      <span class="flex h-7 w-7 items-center justify-center rounded-full bg-gray-200 text-xs font-bold text-gray-600">
                        {{ getInitials(ticket.assigned_to) }}
                      </span>
                      <span>{{ ticket.assigned_to || 'Unassigned' }}</span>
                    </div>
                  </td>
                  <td class="whitespace-nowrap px-6 py-4 text-sm text-gray-500">{{ formatDate(ticket.created_at) }}</td>
                  <td class="whitespace-nowrap px-6 py-4 text-center">
                    <div class="flex items-center justify-center gap-2">
                      <button @click="viewTicketDetails(ticket)" class="action-button bg-gray-100 text-gray-700 hover:bg-gray-200" aria-label="View ticket">
                        <EyeIcon class="h-4 w-4" />
                      </button>
                      <button @click="deleteTicket(ticket.id)" class="action-button bg-red-100 text-red-700 hover:bg-red-200" aria-label="Delete ticket">
                        <TrashIcon class="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <nav class="flex items-center justify-between border-t border-gray-200 bg-gray-50/75 px-6 py-3">
            <p class="text-sm text-gray-600">Page {{ currentPage }}</p>
            <div class="flex gap-2">
              <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" class="pagination-button">
                <ChevronLeftIcon class="h-5 w-5" />
                <span>Previous</span>
              </button>
              <button @click="goToPage(currentPage + 1)" :disabled="tickets.length < pageSize" class="pagination-button">
                <span>Next</span>
                <ChevronRightIcon class="h-5 w-5" />
              </button>
            </div>
          </nav>
        </div>

        <div v-else class="text-center rounded-xl border-2 border-dashed border-gray-300 bg-white py-16">
            <TicketIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-4 text-xl font-semibold text-gray-900">No Tickets Found</h3>
            <p class="mt-1 text-sm text-gray-500">Try adjusting your filters or creating a new ticket.</p>
            <button @click="clearFilters" class="mt-6 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700">
              Clear Filters
            </button>
        </div>
      </main>

      <Transition name="modal-fade">
        <div v-if="selectedTicket" @click="closeModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm">
          <div @click.stop class="w-full max-w-3xl rounded-xl bg-white shadow-2xl">
            <header class="flex items-start justify-between border-b border-gray-200 p-6">
              <div>
                <h2 class="text-2xl font-bold text-gray-900">{{ selectedTicket.title }}</h2>
                <p class="font-mono text-sm text-gray-500">{{ selectedTicket.ticket_number }}</p>
              </div>
              <button @click="closeModal" class="-m-2 rounded-full p-2 transition hover:bg-gray-100">
                <XMarkIcon class="h-6 w-6 text-gray-500" />
              </button>
            </header>

            <div class="max-h-[70vh] overflow-y-auto p-6">
              <div class="grid grid-cols-1 gap-x-8 gap-y-6 md:grid-cols-3">
                <div class="md:col-span-2">
                  <h3 class="modal-label">Description</h3>
                  <p class="rounded-lg bg-gray-50 p-4 text-sm leading-relaxed text-gray-700">{{ selectedTicket.description || 'No description provided.' }}</p>
                </div>
                <aside class="space-y-6">
                  <div>
                    <h3 class="modal-label">Status</h3>
                    <StatusBadge :class="getStatusClass(selectedTicket.status)">{{ formatTitle(selectedTicket.status) }}</StatusBadge>
                  </div>
                   <div>
                    <h3 class="modal-label">Priority</h3>
                    <StatusBadge :class="getPriorityClass(selectedTicket.priority)">{{ formatTitle(selectedTicket.priority) }}</StatusBadge>
                  </div>
                  <div>
                    <h3 class="modal-label">Assigned To</h3>
                    <p class="text-sm text-gray-800">{{ selectedTicket.assigned_to || 'Unassigned' }}</p>
                  </div>
                  <div>
                    <h3 class="modal-label">Created On</h3>
                    <p class="text-sm text-gray-800">{{ formatDate(selectedTicket.created_at) }}</p>
                  </div>
                </aside>
              </div>
            </div>
          </div>
        </div>
      </Transition>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
// It's recommended to use an icon library like Heroicons for cleaner templates
import {
  MagnifyingGlassIcon, ArrowPathIcon, ExclamationTriangleIcon,
  EyeIcon, TrashIcon, ChevronLeftIcon, ChevronRightIcon,
  TicketIcon, XMarkIcon
} from '@heroicons/vue/24/outline';

// --- STATE MANAGEMENT ---
const tickets = ref([]);
const loading = ref(true);
const error = ref(null);
const searchKeyword = ref('');
const selectedTicket = ref(null);

const filters = reactive({
  status: '',
  priority: '',
  category: '',
});

const pagination = reactive({
  currentPage: 1,
  pageSize: 10, // A smaller page size is often better for UX
});

// --- API & DATA FETCHING ---
const fetchTickets = async () => {
  loading.value = true;
  error.value = null;
  try {
    const params = new URLSearchParams({
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      ...filters
    });

    // Handle search separately if a keyword exists
    let url = `/api/tickets/`;
    if (searchKeyword.value.trim()) {
      url = `/api/tickets/search/${encodeURIComponent(searchKeyword.value.trim())}?${params}`;
    } else {
      url = `/api/tickets/?${params}`;
    }

    const response = await fetch(url);
    if (!response.ok) throw new Error('Network response was not ok.');

    tickets.value = await response.json();
  } catch (err) {
    error.value = 'Failed to load tickets. Please check your connection and try again.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchTickets);

// --- METHODS ---
const handleSearch = () => {
  pagination.currentPage = 1;
  fetchTickets();
};

const applyFilters = () => {
  pagination.currentPage = 1;
  fetchTickets();
};

const clearFilters = () => {
  Object.keys(filters).forEach(key => filters[key] = '');
  searchKeyword.value = '';
  pagination.currentPage = 1;
  fetchTickets();
};

const goToPage = (page) => {
  if (page < 1) return;
  pagination.currentPage = page;
  fetchTickets();
};

const deleteTicket = async (ticketId) => {
  if (!confirm('Are you sure you want to delete this ticket? This action cannot be undone.')) {
    return;
  }
  try {
    const response = await fetch(`/api/tickets/${ticketId}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete the ticket.');
    // Refresh the list after successful deletion
    fetchTickets();
    // You could also add a success notification here
  } catch (err) {
    error.value = err.message;
  }
};

// --- MODAL HANDLING ---
const viewTicketDetails = (ticket) => {
  selectedTicket.value = ticket;
};

const closeModal = () => {
  selectedTicket.value = null;
};

// --- UTILITY & FORMATTING ---
const formatTitle = (str) => {
  if (!str) return '';
  return str.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  });
};

const getInitials = (name) => {
  if (!name || name === 'Unassigned') return '?';
  return name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
};

// --- DYNAMIC STYLING ---
const getStatusClass = (status) => ({
  'bg-blue-100 text-blue-800': status === 'open',
  'bg-yellow-100 text-yellow-800': status === 'in_progress',
  'bg-orange-100 text-orange-800': status === 'pending',
  'bg-green-100 text-green-800': status === 'resolved',
  'bg-gray-100 text-gray-800': status === 'closed',
});

const getPriorityClass = (priority) => ({
  'bg-green-100 text-green-800': priority === 'low',
  'bg-yellow-100 text-yellow-800': priority === 'medium',
  'bg-orange-100 text-orange-800': priority === 'high',
  'bg-red-100 text-red-800': priority === 'critical',
});

// Dummy components for demonstration - in a real app, these would be in their own files.
const FilterSelect = {
  props: ['modelValue', 'label', 'defaultOption'],
  template: `
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">{{ label }}</label>
      <select
        :value="modelValue"
        @change="$emit('update:modelValue', $event.target.value)"
        class="w-full rounded-lg border-gray-300 shadow-sm transition duration-150 ease-in-out focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50"
      >
        <option value="">{{ defaultOption }}</option>
        <slot></slot>
      </select>
    </div>
  `
};

const StatusBadge = {
  template: `<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"><slot></slot></span>`
};
</script>

