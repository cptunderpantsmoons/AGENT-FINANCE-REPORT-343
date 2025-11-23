        # Calculate totals
        data['total_current_assets'] = sum(data['current_assets'].values())
        data['total_non_current_assets'] = sum(data['non_current_assets'].values())
        data['total_assets'] = data['total_current_assets'] + data['total_non_current_assets']
        
        data['total_current_liabilities'] = sum(data['current_liabilities'].values())
        data['total_non_current_liabilities'] = sum(data['non_current_liabilities'].values())
        data['total_liabilities'] = data['total_current_liabilities'] + data['total_non_current_liabilities']
        
        data['total_equity'] = sum(data['equity'].values())
        data['total_liabilities_and_equity'] = data['total_liabilities'] + data['total_equity']