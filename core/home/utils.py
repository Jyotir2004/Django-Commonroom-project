from django.contrib.auth import get_user_model

from .models import WorkspaceInvite


def dashboard_context(user=None):
    sample_people = [
        {'name': 'John Carter', 'email': 'john.carter@example.com', 'role': 'Product Designer', 'team': 'Design', 'status': 'Active', 'age': 30, 'account_type': 'Workspace member'},
        {'name': 'Jane Cooper', 'email': 'jane.cooper@example.com', 'role': 'Engineering Manager', 'team': 'Engineering', 'status': 'Active', 'age': 25, 'account_type': 'Workspace member'},
        {'name': 'Alex Morgan', 'email': 'alex.morgan@example.com', 'role': 'Frontend Developer', 'team': 'Engineering', 'status': 'Active', 'age': 28, 'account_type': 'Workspace member'},
        {'name': 'Priya Shah', 'email': 'priya.shah@example.com', 'role': 'People Partner', 'team': 'People', 'status': 'Away', 'age': 32, 'account_type': 'Workspace member'},
        {'name': 'Marcus Lee', 'email': 'marcus.lee@example.com', 'role': 'Content Strategist', 'team': 'Marketing', 'status': 'Active', 'age': 27, 'account_type': 'Workspace member'},
        {'name': 'Sofia Ramirez', 'email': 'sofia.ramirez@example.com', 'role': 'UX Researcher', 'team': 'Design', 'status': 'Active', 'age': 29, 'account_type': 'Workspace member'},
        {'name': 'Noah Williams', 'email': 'noah.williams@example.com', 'role': 'Data Analyst', 'team': 'Operations', 'status': 'Away', 'age': 31, 'account_type': 'Workspace member'},
        {'name': 'Amara Okafor', 'email': 'amara.okafor@example.com', 'role': 'Backend Developer', 'team': 'Engineering', 'status': 'Active', 'age': 26, 'account_type': 'Workspace member'},
        {'name': 'Ethan Brooks', 'email': 'ethan.brooks@example.com', 'role': 'Finance Lead', 'team': 'Finance', 'status': 'Active', 'age': 35, 'account_type': 'Workspace member'},
        {'name': 'Mei Chen', 'email': 'mei.chen@example.com', 'role': 'Visual Designer', 'team': 'Design', 'status': 'Active', 'age': 24, 'account_type': 'Workspace member'},
        {'name': 'Oliver James', 'email': 'oliver.james@example.com', 'role': 'Customer Success', 'team': 'Operations', 'status': 'Away', 'age': 33, 'account_type': 'Workspace member'},
        {'name': 'Lina Haddad', 'email': 'lina.haddad@example.com', 'role': 'Marketing Manager', 'team': 'Marketing', 'status': 'Active', 'age': 30, 'account_type': 'Workspace member'},
    ]
    vegetables = [
        {'name': 'Carrot', 'color': 'Orange', 'type': 'Root'},
        {'name': 'Broccoli', 'color': 'Green', 'type': 'Flower'},
        {'name': 'Spinach', 'color': 'Dark Green', 'type': 'Leaf'},
    ]
    User = get_user_model()
    registered_users = []
    invites = []
    if user and user.is_authenticated:
        registered_users = [
            {
                'name': account.get_full_name() or account.get_username(),
                'email': account.email,
                'role': 'Registered user',
                'team': '—',
                'age': '—',
                'status': 'Active' if account.member_status.is_available else 'Inactive',
                'account_type': 'Registered user',
                'is_self': account.pk == user.pk,
            }
            for account in User.objects.select_related('member_status').order_by('username')
        ]
        invites = [
            {
                'name': invite.name,
                'email': invite.email,
                'role': invite.role,
                'team': invite.team,
                'status': 'Invited',
                'age': '—',
                'account_type': 'Invitation',
                'invite_id': invite.pk,
            }
            for invite in WorkspaceInvite.objects.filter(owner=user).order_by('name')
        ]
    people = sample_people + registered_users + invites
    return {
        'people': people,
        'registered_users': registered_users,
        'vegetables': vegetables,
        'people_count': len(people),
        'active_count': sum(person['status'] == 'Active' for person in people),
        'away_count': sum(person['status'] in ('Away', 'Inactive') for person in people),
        'team_count': len({
            person['team'] for person in people
            if person['team'] != '—'
        }),
    }
