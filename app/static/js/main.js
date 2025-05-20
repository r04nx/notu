$(document).ready(function() {
    // Toggle dark mode
    $('#theme-toggle-btn').click(function() {
        $('body').toggleClass('dark-mode');
        
        if ($('body').hasClass('dark-mode')) {
            $(this).find('i').removeClass('fa-moon').addClass('fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            $(this).find('i').removeClass('fa-sun').addClass('fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        $('body').addClass('dark-mode');
        $('#theme-toggle-btn').find('i').removeClass('fa-moon').addClass('fa-sun');
    }
    
    // Close alert messages
    $('.close-alert').click(function() {
        $(this).closest('.alert').fadeOut();
    });
    
    // Dropdown menu
    $('.dropdown-btn').click(function(e) {
        e.stopPropagation();
        $(this).next('.dropdown-content').toggleClass('show');
    });
    
    // Close dropdown when clicking outside
    $(document).click(function() {
        $('.dropdown-content').removeClass('show');
    });
});
