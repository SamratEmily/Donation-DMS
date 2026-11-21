// DataTables Configuration for Admin List Views
$(document).ready(function() {
    // Default configuration for all DataTables
    var defaultConfig = {
        "pageLength": 25,
        "order": [[0, "desc"]],
        "language": {
            "emptyTable": "No data available",
            "zeroRecords": "No matching records found"
        },
        "dom": 'Bfrtip',
        "buttons": [
            'copy', 'csv', 'excel', 'print'
        ]
    };
    
    // Initialize DataTables for tables with appropriate IDs
    if ($('#donationsTable').length) {
        $('#donationsTable').DataTable(defaultConfig);
    }
    
    if ($('#volunteersTable').length) {
        $('#volunteersTable').DataTable(defaultConfig);
    }
    
    if ($('#donorsTable').length) {
        $('#donorsTable').DataTable(defaultConfig);
    }
    
    if ($('#areasTable').length) {
        $('#areasTable').DataTable(defaultConfig);
    }
});


